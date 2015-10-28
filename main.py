import pprint
import os
from functions import *
from read_data import wiki_data, omdb_data

# import matplotlib.pyplot as plt
# from collections import Counter

pp = pprint.PrettyPrinter(indent=4)

# WIKI DATA
path = '/home/artoo/Workspace_local/Python/Final_Project_02806/data/wiki'
infoboxes, receptions, episode_dic, season_dic, series_length = get_infobox(wiki_data)
num_files = sum([len(files) for r, d, files in os.walk(path)])
sentiment_score = get_score_list()

# OMDB DATA
#omdb_get_genre_avg()


print "\n---------------"

print "Number of downloaded files from Wikipedia: %s" % num_files
print "Number of extracted American TV series(Wiki): %s" % sum(len(i) for i in wiki_data)
print "Number of extracted American TV series(OMDB): %s\n" % sum(len(i) for i in omdb_data)
print "Found infobox in %s serials" % len(infoboxes)
#print "Found receptions in %s serials" % len(receptions)
#print "\nSentiment Analysis Dictionary length: %s" % len(sentiment_score)



# print "\nDisplay the top 10 genres:"
# cnt = Counter(genres_list)
# n_items = take(10, cnt.iteritems())

# PLOTS WIKI
show_series_by_decade(wiki_data)
#show_pies_with_data_loss(count_series, count_none_infoboxes, count_none_titles, count_none_genres, count_none_episodes)
top_shows_by_number_of_episodes(episode_dic)
top_shows_by_season(season_dic)
plot_pagelen_hist(series_length)
plot_sentiment_score(sentiment_score, receptions)
# ~ PLOTS WIKI

# PLOTS OMDB
genre_average, ind, age = omdb_get_data(omdb_data)

print age

width = 0.8
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Genres Rating', fontsize=20)

ax = plt.subplot(111)
ax.bar(range(0, len(genre_average)), genre_average.values(), width, color='r', align='center')
ax.set_xticks(np.arange(len(genre_average.keys())) + width / 2)
ax.set_xticklabels(ind, rotation=90)
plt.grid()
plt.ylim([0, 10])
plt.xlabel('Genre')
plt.ylabel('Rating')

plt.show()
# ~ PLOTS OMDB

# PRINTS
# print cnt
# pp.pprint(receptions)
# pp.pprint(infoboxes)
# pp.pprint(n_items)
# pp.pprint(genres_list)
# pp.pprint(episodes_list)
# pp.pprint(omdb_data)
# ~ PRINTS


# from functions import *
# from imdbpie import Imdb
# imdb = Imdb(anonymize=True, cache=True) # to proxy requests
#
# series = load_series_from_pickle()
#
# for x in filter(lambda g: not g["imdbRating"] == "N/A", series)[:10]:
#      print x["Title"]
#      print x["imdbRating"]
#      print x["imdbID"]
#
#      # getting comments from imdb
#      imdb.get_title_reviews(x["imdbID"])