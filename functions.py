from __future__ import unicode_literals
from itertools import islice
from sklearn.feature_extraction.text import CountVectorizer
from operator import itemgetter
from collections import Counter

import numpy as np
import pickle
import matplotlib.pyplot as plt
import json
import csv
import codecs
import urllib2
import os
import re
import unicodedata
import string


def extract_infobox(serial):

    """ Extract the infobox from wiki pages """

    infobox_reg = re.compile(ur'{{(Infobox|infobox)(.+?)}}', re.DOTALL)

    reg = re.search(infobox_reg, serial)

    if reg is not None:
        infobox = reg.group()
        return infobox
    else:
        return None


def extract_infobox_genre(infobox):

    """ Extract the genre of each serial """

    genre_reg = re.compile(ur'^\|\s*?genre\s*?=(.+?)\n', re.MULTILINE)
    genre = re.search(genre_reg, infobox)

    if genre is not None:
        genres = genre.group(1)
        if len(genres) < 1:
            return None
        else:
            return genres


def extract_infobox_num_seasons(infobox):
 
    """ Extract the number of seasons for each serial/TV Programm """

    season_reg = re.compile(ur'^\|\s*?num_seasons\s*?=(.+?)\n', re.MULTILINE)
    season = re.search(season_reg, infobox)
    
    if season is not None:
        
        num_season = season.group(1)
        if len(num_season) < 1:
            return None
        else:
            clean_num_reg = re.compile(ur'[0-99999]+')            
            clean_num = re.search(clean_num_reg, num_season)
            
            if clean_num is not None:
                clean_num2 = clean_num.group()
                return clean_num2          
                    
                                
def extract_infobox_num_episodes(infobox):
 
    """ Extract the number of episode for each serial """

    episode_reg = re.compile(re.compile(ur'^\|\s*?num_episodes\s*?=(.+?)\n', re.MULTILINE))
    episode = re.search(episode_reg, infobox)

    if episode is not None:
        num_episodes = episode.group(1)

        if len(num_episodes) <= 1:
            return None

        else:
            clean_num_reg = re.compile(ur'[0-99999]+')            
            clean_num = re.search(clean_num_reg, num_episodes)

            if clean_num is not None:
                clean_num2 = clean_num.group()

                return clean_num2


def extract_infobox_name(infobox):

    """ Extract the title of serial  """

    name_reg = re.compile(ur'^\|\s*?(show_name|name)\s*?=(.+?)\n', re.MULTILINE)
    name = re.search(name_reg, infobox)

    if name is not None:
        title = name.group(1)
        return title
    else:
        return None


def get_infobox(decades):

    infoboxes = {}
    receptions = {}

    titles_list = []
    genres_list = []
    episodes_list = []
    episodes_dic={}
    season_dic={}
    series_length={}
    print "Extracting Infobox from data Set..."
    for decade in decades:

        for title, content in decade.items():
            # print title
            #find the length of each page
	    series_length[title] = len(content)
            # GET Reception
            reception = extract_reception(content)
            if reception is not None:
                receptions[title] = reception

            # GET infobox
            infobox = extract_infobox(content)

            if infobox is not None:
                infoboxes[title] = infobox

                # GET Basic Info
                info_title, genre, episode, season = basic_info = get_basic_info(infobox)

                if info_title is not None:
                    titles_list.append(info_title)

                if genre is not None:
                    genres_list.append(genre)

                if episode is not None:
                    episodes_list.append(episode)
                    episodes_dic[title]= int(episode)

                if season is not None:
                    season_dic[title]  = int(season)
                   
    return infoboxes, receptions, episodes_dic, season_dic, series_length


def get_basic_info(infobox):

    """ Extract the basic_info from serial  """

    # GET Title of serial
    title = extract_infobox_name(infobox)

    # GET Genres of serial
    genre = extract_infobox_genre(infobox)

    # GET Number of Episodes
    episode = extract_infobox_num_episodes(infobox)
    
    # GET Number of Seasons
    season = extract_infobox_num_seasons(infobox)

    return title, genre, episode, season


def take(n, iterable):

    """ Return first n items of the iterable as a list """

    return list(islice(iterable, n))


def show_series_by_decade(all_decades):

    """ Plots a bar chart with the productions per decade """

    series = []

    for i in all_decades:
        series.append(len(i))

    ind = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
    width = 0.8

    fig = plt.figure()
    fig.suptitle('TV Series production by decade', fontsize=20)

    ax = plt.subplot(111)

    ax.bar(range(len(ind)), series, width, color='r')
    ax.set_xticks(np.arange(len(ind)) + width / 2)
    ax.set_xticklabels(ind, rotation=90)

    # add some text for labels, title
    plt.xlabel('Decades')
    plt.ylabel('Number of productions')

    plt.show()


def show_pies_with_data_loss(count_series, count_none_infoboxes, count_none_titles, count_none_genres, count_none_episodes):

    """ Plots pies in a singles figure to display the loss of data when mining """

    labels_1 = 'Valid Series', 'No Infobox'
    labels_2 = 'Valid Series', 'No Title'
    labels_3 = 'Valid Series', 'No Genre'
    labels_4 = 'Valid Series', 'No Episodes'

    sizes_1 = [count_series - count_none_infoboxes, count_none_infoboxes]
    sizes_2 = [count_series - count_none_titles, count_none_titles]
    sizes_3 = [count_series - count_none_genres, count_none_genres]
    sizes_4 = [count_series - count_none_episodes, count_none_episodes]

    colors = ['lightskyblue', 'gold']
    explode = (0, 0.1)

    fig = plt.figure(1)
    fig.suptitle('Wikipedia data Mining Results', fontsize=20)

    plt.subplot(221)
    plt.pie(sizes_1, explode=explode, labels=labels_1, colors=colors, autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')

    plt.subplot(222)
    plt.pie(sizes_2, explode=explode, labels=labels_2, colors=colors, autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')

    plt.subplot(223)
    plt.pie(sizes_3, explode=explode, labels=labels_3, colors=colors, autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')

    plt.subplot(224)
    plt.pie(sizes_4, explode=explode, labels=labels_4, colors=colors, autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')

    plt.show()


def plot_pagelen_hist(series_length):  

    """ after reading pages count the page length and make a histogram """

    series_keys, series_values = zip(*series_length.items())
    num_bins = len(series_length) / 20

    # plot top 10 page lengths
    sorted_series = sorted(series_length.items(), key=itemgetter(1), reverse=True)
    series_keys_sorted, series_values_sorted = zip(*sorted_series)
    
    fig = plt.figure(1)
    fig.suptitle('Wikipedia data Mining Results', fontsize=20)

    plt.subplot(211)
    plt.hist(series_values, num_bins, color='red')

    plt.xlabel('Number of Characters in Page')
    plt.ylabel('Number of Pages')
    
    plt.subplot(212)
    plt.bar(np.arange(1, 11), series_values_sorted[:10], color='yellow')
    
    plt.xlabel('TV Series')
    plt.ylabel('No of Characters in Wiki Pages')
    plt.xticks(np.arange(1, 11), series_keys_sorted[:10], rotation=45)
    
    plt.show()


def top_shows_by_number_of_episodes(episode_dic):  

    """ find the top-10 lifelong series and shows """

    sorted_episode = sorted(episode_dic.items(), key=itemgetter(1), reverse=True)

    episode_keys, episode_values = zip(*sorted_episode)

    plt.figure(figsize=(17, 8))
    plt.bar(np.arange(1, 11), episode_values[:10], color='blue')
    
    plt.xlabel('TV Shows')
    plt.ylabel('No of Episodes')
    plt.xticks(np.arange(1, 11), episode_keys[:10], rotation=45)

    plt.show()


def clean(input):

    # internal links
    links = re.compile(ur'\[\[([^\]]+?)(?:\|(.+?))?\]\]')

    # references category links urls
    allclean = ref = re.compile(ur'<ref(.+?)</ref>|<ref(.+?)\/>|{{(.+?)}}|\'{2,}|\[\[Category:(.+?)\]\]|\[http://.+?\]')

    # infobox
    citgreed = re.compile(ur'{{(.+?)}}', re.DOTALL)

    # quotes
    quote = re.compile(ur'{{quote\|(.+?)\}}')

    output = re.sub(quote, lambda m: m.group(1) , input)
    output = re.sub(allclean, "", output)
    output = re.sub(links, lambda m: filter(None, m.groups())[-1] , output)
    output = re.sub(citgreed, "", output)

    return output


def extract_reception(serial):

    """ Extract the Reception text from json file """

    reception_reg = re.compile(ur'==(Reception|Response|)==(.+)==(\w+)==', re.DOTALL)

    reg = re.search(reception_reg, serial)

    if reg is not None:
        reception = reg.group()
        return clean(reception)
    else:
        return None


def get_score_list():

    """ Create and return a dictionary with words and their sentiment score  """

    reader = csv.reader(open("include/Ratings_Warriner_et_al.csv"))

    head = reader.next()

    word = head.index('Word')
    v = head.index('V.Mean.Sum')
    a = head.index('A.Mean.Sum')
    d = head.index('D.Mean.Sum')

    anew = {row[word]: [float(row[v]) - 5, float(row[a]) - 5, float(row[d]) - 5] for row in reader}

    return anew


def score(anew, documents, weights):

    """ Create and return a dictionary with words and their sentiment score  """

    test = CountVectorizer(vocabulary=anew.keys())
    x = test.fit_transform(documents)

    return (x * np.matrix(weights)) / x.sum(axis=1)


def plot_sentiment_score(anew, receptions):

    """
        Takes the score list and the text to perform sentiment analysis.
        Display a scatter plot with the scores.
    """

    fig = plt.figure(figsize=(12, 8))
    fig.suptitle('Sentiment Analysis on Wiki Receptions', fontsize=20)

    x = score(anew, receptions.values(), np.matrix(anew.values())[:, 0])
    y = score(anew, receptions.values(), np.matrix(anew.values())[:, 2])
    plt.scatter(x, y, marker='.', label='', color='green')

    plt.xlabel('valence')
    plt.ylabel('domination')

    plt.show()


def extract_omdb_data(omdb_data):

    """ Count the genres and the occurrences in the data set """

    genre = []
    new = {}

    gencon = Counter()
    age = Counter()

    for x, v in omdb_data.iteritems():

        new[string.lower(x)] = v

        genre = v["Genre"].split(",")
        genre = map(lambda s: s.strip(), genre)

        rated = v["Rated"].split(",")
        rated = map(lambda s: s.strip(), rated)

        gencon.update(genre)
        age.update(rated)


def make_bar_plot(dic, x_lbl, y_lbl, sup_title, width=0.6, color='r'):

    """ Creates a bar chart from a dictionary """
    val = []
    ke = []
    for k, v in dic.iteritems():
        ke.append(k)
        val.append(v)

    fig = plt.figure()
    fig.suptitle(sup_title, fontsize=20)

    ax = plt.subplot(111)
    ax.bar(range(len(ke)), val, width, color, align='center')
    ax.set_xticks(np.arange(len(ke)) + width / 2)
    ax.set_xticklabels(dic.keys(), rotation=90)
    plt.xlabel(x_lbl)
    plt.ylabel(y_lbl)

    plt.show()


def load_series_from_pickle(path="data/imdb/save.p"):

    """ Load series from a pickle file """

    print "Loading data from %s ..." % path
    omdb_data = pickle.load(open(path, "rb"))
    print "Done\n"

    series = {}
    for x, v in omdb_data.iteritems():
        series[x] = v

    return series


def omdb_get_data(omdb_data):

    """   """
    omdb_rated = []
    genre_avg = {}
    genres = []
    rating = []
    rated = []
    ind = []
    c_genres = Counter()

    age = Counter()

    rating_genres = {}
    for i in omdb_data:
        for x, v in i.iteritems():
            omdb_imdbRating = v["imdbRating"]
            if omdb_imdbRating != 'N/A':
                rating.append(omdb_imdbRating)

            omdb_Genre = v['Genre'].split(",")
            if omdb_Genre != 'N/A':
                omdb_Genre = map(lambda s: s.strip(), omdb_Genre)
                if omdb_imdbRating != 'N/A':
                    for i in omdb_Genre:
                        if rating_genres.has_key(i):
                            rating_genres[i].append(float(omdb_imdbRating))
                        else:
                            rating_genres[i] = [float(omdb_imdbRating)]
                genres.append(omdb_Genre)
            c_genres.update(omdb_Genre)

            rated = v["Rated"].split(",")
            rated = map(lambda s: s.strip(), rated)

            age.update(rated)

        # age['Unrated'] = age['Unrated'] + age['Not Rated'] + age['NOT RATED']
        # del age['Not Rated']
        # del age['NOT RATED']
        # age = sorted(age.most_common(), key=lambda tup: tup[1], reverse=True)

    for k, v in rating_genres.iteritems():
        ind.append(k)
        average = (sum(v) / float(len(v)))
        genre_avg[k] = float(format(round(average, 2)))

    return genre_avg, ind, age


def top_shows_by_season(season_dic):

    # find the top-10 lifelong series and shows 

    sorted_season = sorted(season_dic.items(), key=itemgetter(1), reverse=True)
    season_keys, season_values = zip(*sorted_season)

    plt.figure(figsize=(17, 8))
    plt.bar(np.arange(1, 11), season_values[:10], color='blue')
    
    plt.xlabel('TV Shows')
    plt.ylabel('No of seasons')
    plt.xticks(np.arange(1, 11), season_keys[:10], rotation=45)
    plt.show()


def plot_pagelen_hist(series_length):  
    
    series_keys,series_values = zip(*series_length.items())
    numBins = len(series_length)/20
    
    
    #plot top10 page lengths
    sorted_series = sorted(series_length.items(), key=itemgetter(1), reverse=True)
    series_keys_sorted,series_values_sorted = zip(*sorted_series)
    
    
   
    
    fig = plt.figure(1)
    fig.suptitle('Wikipedia Data Mining Results', fontsize=20)

    plt.subplot(211)
    plt.hist(series_values,numBins,color='red')
    plt.xlabel('Number of Characters in Page')
    plt.ylabel('Number of Pages')
    
    plt.subplot(212)
    plt.bar(np.arange(1,11),series_values_sorted[:10], color='yellow')
    
    plt.xlabel('TV Series')
    plt.ylabel('No of Characters in Wiki Pages')
    plt.xticks( np.arange(1,11), series_keys_sorted[:10], rotation=45 )
    
    plt.show()