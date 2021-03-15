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
# import names
import gender_guesser.detector as gender
import calendar
from random_word import RandomWords

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
    r = RandomWords()
    i = random.randint(0, 9)
    if i == 0:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="verb") + " the " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 1:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 2:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective")).title()
    if i == 3:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 4:
        return ("The " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 5:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun") + " " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 6:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun") + " and " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 7:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun") + " or " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")).title()
    if i == 8:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="verb") + " " + random.choice(["me", "you", "her", "him"]))
    if i == 9:
        return (r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="verb") + "ing in the " + r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun"))


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

# ## Replace Names (doesn't work currently)
# https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk
# Shivansh bhandari's answer

# In[8]:


# person_list = []
# person_names=person_list
# def get_human_names(text):
#     tokens = nltk.tokenize.word_tokenize(text)
#     pos = nltk.pos_tag(tokens)
#     sentt = nltk.ne_chunk(pos, binary = False)

#     person = []
#     name = ""
#     for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
#         for leaf in subtree.leaves():
#             person.append(leaf[0])
#         if len(person) > 1: #avoid grabbing lone surnames
#             for part in person:
#                 name += part + ' '
#             if name[:-1] not in person_list:
#                 person_list.append(name[:-1])
#             name = ''
#         person = []
# #     print (person_list)

# names_ = get_human_names(text)
# for person in person_list:
#     person_split = person.split(" ")
#     for name in person_split:
#         if wordnet.synsets(name):
#             if(name in person):
#                 person_names.remove(person)
#                 break

# print(person_names)


# TODO: function to replace names with autogen names
# maybe create dict that matches old to new
# also need to replace last names as well as first names (maybe first names too?)
# i think can replace all full names, then can look for last or first because shouldn't be an issue that we already replaced some

# In[24]:


# name_genders = {}
# d = gender.Detector()
# for name in person_names:
#     g = d.get_gender(name.split()[0])
#     print(name, g)
#     if g == 'male' or g == 'female':
#         name_genders[name] = g
# name_genders


# # In[25]:


# name_replacements = {}
# for k,v in name_genders.items():
#     name_replacements[k] = names.get_full_name(gender=v)
# name_replacements


# # In[26]:


# for k,v in name_replacements.items():
#     text = re.sub(k.split()[0], v.split()[0], text) # replace first name
#     text = re.sub(k.split()[1], v.split()[1], text) # replace last name


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
        text = re.sub('\[SONG_NAME\]',  "\"" + random_song_name() + "\"", text)
        return_texts.append(text)
    return return_texts

def replace_albums(texts):
    return_texts = []
    for text in texts:
        text = re.sub('\[ALBUM_NAME\]', random_song_name(), text)
        return_texts.append(text)
    return return_texts

# In[14]:


with open('data/consolidatedData.json', 'r', encoding='utf-8') as inf:
    paras = json.load(inf)

#with open('data/0.json', 'r', encoding='utf-8') as inf:
#    data = json.load(inf)
para = paras['allPrunedParaComplete'][3]
print(para)
print("")
new_name, para = replace_band_name(para)
para = replace_years(para)
para = replace_months(para)
para = replace_genre(para)
para = replace_albums(para)
para = replace_songs(para)
print(para)


# In[ ]:

def replace(texts):
   new_name, texts = replace_band_name(texts)
   texts = replace_years(texts)
   texts = replace_months(texts)
   texts = replace_genre(texts)
   texts = replace_albums(texts)
   texts = replace_songs(texts)
   return texts, new_name
