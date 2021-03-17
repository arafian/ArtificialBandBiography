#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import re
from datetime import datetime
import random
import nltk
import pickle
from nameparser.parser import HumanName
from nltk.corpus import wordnet
import gender_guesser.detector as gender
import calendar
import names
from wonderwords import RandomWord

# ## Replace Band Name

# In[4]:


with open('titles', 'rb') as inf:
    titles = pickle.load(inf)

determiners = []
nouns = []
adjectives = []
for title in titles:
    tagged_title = nltk.pos_tag(nltk.word_tokenize(title.lower()))
    for tagged_word in tagged_title:
        word = tagged_word[0]
        pos = tagged_word[1]
        if pos == 'DT':
            determiners.append(word)
        elif pos == 'NN' or pos == 'NNS':
            nouns.append(word.capitalize())
        elif pos == 'JJ':
            adjectives.append(word.capitalize())


# In[5]:

def random_song_name():
    r = RandomWord()
    i = random.randint(0, 9)
    if i == 0:
        return (r.word(include_parts_of_speech=["verbs"]) + " the " + r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 1:
        return (r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 2:
        return (r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["adjectives"])).title()
    if i == 3:
        return (r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 4:
        return ("The " + r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 5:
        return (r.word(include_parts_of_speech=["nouns"]) + " " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 6:
        return (r.word(include_parts_of_speech=["nouns"]) + " and " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 7:
        return (r.word(include_parts_of_speech=["nouns"]) + " or " + r.word(include_parts_of_speech=["nouns"])).title()
    if i == 8:
        return (r.word(include_parts_of_speech=["verbs"]) + " " + random.choice(["me", "you", "her", "him"])).title()
    if i == 9:
        return (r.word(include_parts_of_speech=["verbs"]) + "ing in the " + r.word(include_parts_of_speech=["nouns"])).title()


def replace_band_name(texts):
    def getRandName():
        determiner = random.choice(determiners).capitalize()
        [adjective1, adjective2] = random.sample(adjectives, 2)
        [noun1, noun2] = random.sample(nouns, 2)

        title_format = random.randrange(3)
        if title_format == 0:
            return determiner + ' ' + adjective1 + ' ' + noun1
        elif title_format == 1:
            return determiner + ' ' + adjective1 + ' ' + adjective2 + ' ' + noun1
        elif title_format == 2:
            return determiner + ' ' + noun1 + ' and ' + determiner + ' ' + noun2

    new_name = getRandName()
    return_texts = []
    for text in texts:
      text = re.sub('\[BAND_NAME\]', new_name, text)
      return_texts.append(text)
    return new_name, return_texts


# ## Replace Years

# In[6]:


def replace_years(texts):
    num_years = ''.join(texts).count('[YEAR]')
    first_year = datetime.now().year - (5 * num_years)
    years = [first_year]
    for i in range(1, num_years):
        years.append(years[i-1] + random.randint(0, 5))

    j = -1
    def get_year(matchobj):
        nonlocal j
        j += 1
        return years[j]

    return_texts = []
    for text in texts:
       text = re.sub("\[YEAR\]", lambda x: str(get_year(x)), text)
       return_texts.append(text)
    return return_texts


# ## Replace Months

# In[7]:


def replace_months(texts):
    months = [calendar.month_name[i] for i in range(1,13)] + [calendar.month_abbr[i] for i in range(1,13)]
    return_texts = []
    for text in texts:
       text = re.sub('\[MONTH\]', lambda x: random.choice(months), text)
       return_texts.append(text)

    return return_texts

# ## Replace Names

def replace_person_names(texts):
    return_texts = []
    for text in texts:
        full_name_genders = {}
        for k in re.findall('PERSON_NAME_FULL_._(?:MALE|FEMALE)', text):
            if k[-6:] == 'FEMALE':
                full_name_genders[k] = 'female'
            else:
                full_name_genders[k] = 'male'

        full_name_replacements = {}
        for k,v in full_name_genders.items():
            full_name_replacements[k] = names.get_full_name(gender=v)

        # replace full names
        for k,v in full_name_replacements.items():
            text = re.sub(k, v, text)

        # replace last names
        for k in re.findall('PERSON_NAME_LAST_.', text):
            # get corresponding last name from full names by person number
            last_name = None
            for name_key in full_name_replacements.keys():
                person_num = k[-1]
                if person_num in name_key:
                    last_name = full_name_replacements[name_key].split()[1]

            if last_name:
                text = re.sub(k, last_name, text)
            else:
                text = re.sub(k, random.choice(['Ngo', 'Movva', 'Rafian', 'Jain']), text) # easter egg

        # replace first names
        for k in re.findall('PERSON_NAME_FIRST_.', text):
            # get corresponding first name from full names by person number
            first_name = None
            for name_key in full_name_replacements.keys():
                person_num = k[-1]
                if person_num in name_key:
                    first_name = full_name_replacements[name_key].split()[0]

            if first_name:
                text = re.sub(k, first_name, text)
            else:
                text = re.sub(k, random.choice(['James', 'Mani', 'Arman', 'Ishaan']), text) # easter egg

        return_texts.append(text)

    return return_texts

# ## Replace Genre

# ### Get all Genres

# In[9]:


with open('data/consolidatedData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

genres = set()
for genre in data['allGenres']:
    if isinstance(genre, str):
        g = re.split(',|\[', genre)[0]
        genres.add(g)

genres = list(genres) # need to convert to list to be able to take a random choice from it


# In[10]:


def replace_genre(texts):
    new_genre = random.choice(genres)
    return_texts = []
    for text in texts:
      text = re.sub('\[GENRE\]', new_genre, text)
      return_texts.append(text)
    return return_texts


# ## Replace All Placeholders

def replace_songs(texts):
    return_texts = []
    for text in texts:
        try:
            text = re.sub('\[SONG_NAME\]',  "\"" + random_song_name() + "\"", text)
            return_texts.append(text)
        except:
           return_texts.append(text)
    return return_texts

def replace_albums(texts):
    return_texts = []
    for text in texts:
        try:
            text = re.sub('\[ALBUM_NAME\]', random_song_name(), text)
            return_texts.append(text)
        except:
            return_texts.append(text)
    return return_texts



# In[ ]:

def replace(texts):
    texts = replace_albums(texts)
    texts = replace_songs(texts)
    new_name, texts = replace_band_name(texts)
    texts = replace_years(texts)
    texts = replace_months(texts)
    texts = replace_genre(texts)

    texts_new = []
    for t in texts:
        texts_new.append(re.sub('\[|\]', '', t)) # need to get rid of brackets to be able to replace names using re.sub

    texts = texts_new
    texts = replace_person_names(texts)
    return texts, new_name
