import pickle
import codecs
import json
import os


def read_decade(folder):

    """ Read downloaded data from files"""

    path = "/home/artoo/Workspace_local/Python/Final_Project_02806/data/wiki/" + folder + "/"
    file_list = os.listdir(path)
    decade = {}

    for each_file in file_list:

        each_file = codecs.open(path + each_file, 'r', 'utf-8')
        try:
            source = json.loads(each_file.read())
        except ValueError as ve:
            print "\nError while reading series..."
            print ve.message + "\n"

        title = source['query']['pages'].itervalues().next()['title']
        content = source['query']['pages'].itervalues().next()['revisions'][0]['*']


        decade[title] = content

    return decade


# Read wiki data
print 'Reading wiki data...'
wiki_1930 = read_decade('series_1930')
wiki_1940 = read_decade('series_1940')
wiki_1950 = read_decade('series_1950')
wiki_1960 = read_decade('series_1960')
wiki_1970 = read_decade('series_1970')
wiki_1980 = read_decade('series_1980')
wiki_1990 = read_decade('series_1990')
wiki_2000 = read_decade('series_2000')
wiki_2010 = read_decade('series_2010')
wiki_data = [wiki_1930, wiki_1940, wiki_1950, wiki_1960, wiki_1970, wiki_1980, wiki_1990, wiki_2000, wiki_2010]

# Read omdb data
print 'Reading omdb data...'
path = '/home/artoo/Workspace_local/Python/Final_Project_02806/data/omdb/'
omdb_1930 = pickle.load(open(path + "omdb_1930.p", "rb"))
omdb_1940 = pickle.load(open(path + "omdb_1940.p", "rb"))
omdb_1950 = pickle.load(open(path + "omdb_1950.p", "rb"))
omdb_1960 = pickle.load(open(path + "omdb_1960.p", "rb"))
omdb_1970 = pickle.load(open(path + "omdb_1970.p", "rb"))
omdb_1980 = pickle.load(open(path + "omdb_1980.p", "rb"))
omdb_1990 = pickle.load(open(path + "omdb_1990.p", "rb"))
omdb_2000 = pickle.load(open(path + "omdb_2000.p", "rb"))
omdb_2010 = pickle.load(open(path + "omdb_2010.p", "rb"))
omdb_data = [omdb_1930, omdb_1940, omdb_1950, omdb_1960, omdb_1970, omdb_1980, omdb_1990, omdb_2000, omdb_2010]

print '\nWIKI lengths %s' % list(len(i) for i in wiki_data)
print 'OMDB lengths %s\n' % list(len(i) for i in omdb_data)



