# John Loeber | 15-OCT-2014 | Python 2.7.6 | Debian Linux | www.johnloeber.com

from bs4 import BeautifulSoup
from collections import Counter
from sys import argv
import urllib2

# returns a string containing an entire year's episode summaries of a show
def parselink(url):
    allstr = ""
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
                    allstr += w + " "
            allstr+='\n'
    return allstr

# takes a wikipedia category (for tv seasons of a given year), finds all the 
# links, calls parselink on all links to get episode summaries from each page
# compiles all such summaries into one text document
def getwords(url,f):
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
        f.write(parselink(l)+'\n\n')
    return
   
def main():
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
            getwords(url,f)

if __name__=='__main__':
    main()
