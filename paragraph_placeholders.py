# -*- coding: utf-8 -*-
"""Paragraph_Placeholders.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sV4qrIAlYw2qT2zEzwccI0GNW1AwHcHE
"""

# pip install gender-guesser
import json
import re
import nltk
from nltk.corpus import wordnet
import calendar
import gender_guesser.detector as gender
import random

"""## Band Name Placeholder"""

def band_placeholder(data, texts):
    band_name = data['Name']
    if '(' in band_name: # some bands have disambiguation in the title such as "Mother Earth (American band)"
        band_name = ' '.join(band_name.split(' (')[:-1])

    return_texts = []
    for text in texts:
        text = re.sub(band_name, '[BAND_NAME]', text)
        return_texts.append(text)

    return return_texts

"""## Year Placeholder"""

def year_placeholder(texts):
    return_texts = []
    for text in texts:
        text = re.sub("[0-9]{4}", '[YEAR]', text)
        return_texts.append(text)
    return return_texts

"""## Month Placeholder"""

def month_placeholder(texts):
    return_texts = []
    for text in texts:
        months = [calendar.month_name[i] for i in range(1,13)] + [calendar.month_abbr[i] for i in range(1,13)]
        for month in months:
            text = re.sub(month, '[MONTH]', text)
        return_texts.append(text)
    return return_texts

"""## Name Placeholder
https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk
Shivansh bhandari's answer
"""

def get_person_names(data, text):
    person_list = []
    person_names=person_list
    def get_human_names(text):
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)

        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []

    names_ = get_human_names(text)
    for person in person_list:
        person_split = person.split(" ")
        for name in person_split:
            if wordnet.synsets(name):
                if(name in person):
                    person_names.remove(person)
                    break

    # add member names from infobox
    if 'infobox' in data.keys():
        members = []
        if 'Members' in data['infobox'].keys():
            members += data['infobox']['Members']

        if 'Past members' in data['infobox'].keys():
            members += data['infobox']['Past members']

        # some members have extra information that needs to be removed such as 'Earl Yager - bass'
        for member in members:
            member = member.split()
            if len(member) > 1:
                member = member[0] + member[1]
            else:
                member = member[0]

            person_names.append(member)

    person_names = set(person_names)
    return person_names

def get_name_genders(person_names):
    name_genders = {}
    d = gender.Detector()
    for name in person_names:
        g = d.get_gender(name.split()[0])
        if 'female' in g:
            name_genders[name] = 'FEMALE'
        elif 'male' in g:
            name_genders[name] = 'MALE'
        elif g == 'andy':
            name_genders[name] = random.choice(['MALE', 'FEMALE'])
        else:
            continue # unknown name

    return name_genders

def person_name_placeholder(data, texts):
    person_names = get_person_names(data, ''.join(texts))
    name_genders = get_name_genders(person_names)
    i = 0
    for name,gender in name_genders.items():
        return_texts = []
        for text in texts:
            text = re.sub(name, '[PERSON_NAME_FULL_' + str(i) + '_' + gender + ']', text)
            if len(name.split()) > 1: # some only have first names
                first = name.split()[0]
                last = name.split()[-1]
                # don't want abbreviations to be subsituted
                if len(first) > 2:
                    text = re.sub(first, '[PERSON_NAME_FIRST_' + str(i) + ']', text) # replace first name

                if len(last) > 2:
                    text = re.sub(last, '[PERSON_NAME_LAST_' + str(i) + ']', text) # replace last name
            return_texts.append(text)
        texts = return_texts
        i += 1

    return texts

"""## Genre Placeholder

### Get all genres
"""

with open('data/consolidatedData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

genres = set()
for genre in data['allGenres']:
    if isinstance(genre, str):
        g = re.split(',|\[', genre)[0]
        genres.add(g)

genres = list(genres) # need to convert to list to be able to take a random choice from it

def genre_placeholder(texts):
    return_texts = []
    for text in texts:
        part2 = re.split(' a | an ', text)
        genre = None
        if len(part2) > 1:
            genre = re.split(' band', part2[1])[0]
        if genre:
            text = re.sub(genre, '[GENRE]', text)

        return_texts.append(text)

    return return_texts

"""## Paragraph Placeholder"""

def get_paragraph_placeholders(data):
    #  with open(json_file, 'r', encoding='utf-8') as f:
    #      data = json.load(f)

    texts = data['rawData']
    texts = band_placeholder(data, texts)
    texts = year_placeholder(texts)
    texts = month_placeholder(texts)
    texts = person_name_placeholder(data, texts)
    texts = album_placeholders(data["albums"], texts)
    texts = song_placeholders(texts)
    try:
        texts = genre_placeholder(texts)
    except:
        pass
    return texts


# print(get_paragraph_placeholder('data/1599.json'))

# for i in range(1657):
#     try:
#         get_paragraph_placeholder('data/' + str(i) + '.json')
#     except:
#         print(i)


def album_placeholders(albums, texts):
    return_texts = []
    for text in texts:
        for i in range(len(albums)):
            return_texts.append(re.sub(rf'{re.escape(albums[i])}', "[ALBUM_NAME]", text))
    return return_texts

def song_placeholders(texts):
    return_texts = []
    for text in texts:
        return_texts.append(re.sub(r'\"(.+)\"', "[SONG_NAME]", text))
    return return_texts



complete_paras = []
for i in range(1657):
    print(i)
    with open('data/' + str(i) + '.json', 'r', encoding='utf-8') as inf:
        data = json.load(inf)
        #try:
        complete_paras.append(get_paragraph_placeholders(data))
        #except:
        #    print(i)
#print(complete_paras)

with open('data/consolidatedData.json', 'r', encoding='utf-8') as inf:
    consol_data = json.load(inf)
    consol_data.update({'allPrunedParaComplete': complete_paras})

with open('data/consolidatedData.json', 'w', encoding='utf-8') as inf:
    json.dump(consol_data, inf, indent=3)
