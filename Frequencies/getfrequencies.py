# John Loeber | 15-OCT-2014 | Python 2.7.6 | Debian Linux | www.johnloeber.com

from bs4 import BeautifulSoup
from collections import Counter
from sys import argv
import urllib2

# Takes a link to a season of a television show. Finds the list of episodes, 
# parses it, and returns a dictionary of word frequencies.
def parselink(url):
    allwords = {}
    global FILTERSTOPWORDS
    if FILTERSTOPWORDS:
        global stopwords
    # this is very inefficient, but works quickly enough.
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    soup = soup.findAll("td", class_="description")
    for x in soup:
        for match in x.findAll('a'):
            match.unwrap()
        for match in x.findAll('p'):
            match.unwrap()
        # split the soup up into individual lines
        z = str(x).lower().split('\n')
        for snip in z:
            # remove formatting
            if "united states</td>" in snip or "<small>" in snip:
                continue
            elif "<b>" in snip and ":" in snip:
                continue
            else:
                # this text processing is faster than bs4's unwrap, etc.
                if  "<td class=" in snip:
                    snip = snip[snip.index(">")+1:]
                while "<span" in snip:
                    newsnip = snip[:snip.index("<span")] + \
                              snip[snip.index("</span>")+7:]
                    # in certain badly-formatted cases, the above doesn't work.
                    if len(newsnip)>=len(snip):
                        break
                    else:
                        snip = newsnip
                while "<sup" in snip:
                    newsnip = snip[:snip.index("<sup")] + \
                              snip[snip.index("</sup>")+6:]
                    if len(newsnip)>=len(snip):
                        break
                    else:
                        snip = newsnip
                snip = snip.replace("</td>","")
                snip = snip.replace("<i>","")
                snip = snip.replace("</i>","")
                snip = snip.replace("<br/>","")
                snip = snip.replace("</br>","")
                snip = snip.replace("<hr/>","")
                snip = snip.replace("</b>","")
                snip = snip.replace("<b>","")
                snip = snip.replace("<ul>","")
                snip = snip.replace("</ul>","")
                snip = snip.replace("<li>","")
                snip = snip.replace("</li>","")
                if "<" in snip or ">" in snip:
                    # for debugging
                    #print snip
                    continue
                #split up the line into individual words
                snip = snip.split(" ")
                for y in snip:
                    # remove punctuation
                    w = y.translate(None, ',.!?\'"()\n;$:[]')
                    if FILTERSTOPWORDS:
                        if w in stopwords:
                            continue   
                    if w in allwords:
                        allwords[w] += 1
                    else:
                        allwords[w] = 1
    if '' in allwords:
        del allwords['']
    if ' ' in allwords:
        del allwords[' ']
    # remove nonwords or garbled words
    for word in allwords.keys():
        if '\\' in word or '<' in word or '>' in word or '/' in word:
            del allwords[word]
    return allwords

# takes a wikipedia category (for tv seasons of a given year), finds all the 
# links, calls parselink on all those links to get word frequencies from each page,
# compiles all word frequency dictionary into one.
def getwords(url):
    allwords = {}
    collectedlinks = []
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r)
    # get links to seasons
    shows = soup.find("div", id="mw-pages")
    links = shows.findAll('a')
    for link in links:
        x = str(link.get('href'))
        if 'season' in x:
            collectedlinks.append("http://en.wikipedia.org"+x)
    # get word frequencies
    for l in collectedlinks:
        # technique from: http://stackoverflow.com/a/11011846
        retdic = Counter(parselink(l))
        allwords = dict(retdic + Counter(allwords))
     #print allwords
    return allwords
    
def main():
    global FILTERSTOPWORDS
    if argv[1].lower()=="y":
        FILTERSTOPWORDS = True
    elif argv[1].lower()=="n":
        FILTERSTOPWORDS = False
    else:
        raise Exception("Erroneous command-line arg. Need 'y' or 'n' to filter"
                        " or not filter stopwords, respectively.")
    if FILTERSTOPWORDS:
        global stopwords
        with open("stopwords-final","r") as h:
            stopwords = filter(lambda y: y!='',[x.replace('\n','') 
                               for x in h.readlines()])

    cat = "http://en.wikipedia.org/wiki/Category:Television_seasons_by_year"
    r = urllib2.urlopen(cat).read()
    soup = BeautifulSoup(r)
    
    divs = soup.findAll("div", class_="CategoryTreeSection")
    urls = []
    for div in divs:
        urls.append("http://en.wikipedia.org" + div.find('a').get('href'))
    # remove entry for 2015
    del urls[-1]

    # process each year
    for index, url in enumerate(urls):
        year = str(index+1950)        
        with open(year,"w") as f:
            print year
            worddict = getwords(url)
            f.write(str(worddict)+'\n'+str(sum(worddict.values())))

if __name__=='__main__':
    main()
