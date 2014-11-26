# John Loeber | Oct-28-2014 | Python 2.7.6 | Debian Linux | www.johnloeber.com

from os import listdir
from sys import argv
from collections import Counter
from ast import literal_eval
from operator import itemgetter

# takes one command-line arg: directory of alltime.py outputs, like "1950", etc.

# from http://stackoverflow.com/a/196392
def is_ascii(x):
    return all(ord(c) < 128 for c in x)

path = argv[1]
listdir = listdir(path)
listdir.sort()
listdir = filter(lambda x: x.isdigit(), listdir)

collected_counter = Counter({})

for i in listdir:
    go = path + i
    with open(go,'r') as f:
        dic = literal_eval(f.read().split('\n')[0])
        collected_counter += Counter(dic)

full = dict(collected_counter)
slashes = dict((x,y) for x,y in full.items() if not is_ascii(x))
repslashes = sorted(slashes.items(), key=itemgetter(1))

print "total number of words:", sum(full.values())
print "number of unique words:", len(full)
print "total number of non-ascii words:", sum(slashes.values())
print "number of unique non-ascii words:", len(slashes)

with open("nonascii","w") as f:
    f.write(str(repslashes)+'\n')
