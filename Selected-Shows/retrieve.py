# John Loeber | Oct 9 2014 | Debian Linux | Python 2.7.6

# This script takes a textfile that is a list of websites. It downloads
# the text from those websites, and saves each text into the current directory.

from bs4 import BeautifulSoup
import sys, urllib2

def load(loc):
    with open(loc) as f:
        return f.readlines()

# argv[1] is website list
def main():
    with open(sys.argv[1]) as f:
        for index, line in enumerate(f):
            url = line.rstrip('\r\n')
            html = urllib2.urlopen(url).read()

            soup = BeautifulSoup(html)
            for match in soup.findAll('a'):
                match.unwrap()
            for match in soup.findAll('p'):
                match.unwrap()
            soup = soup.findAll("td", class_="description")
            f = open("souped_"+str(index),'w')
            for x in soup:
                y = str(x)
                z = y.split('\n')
                for snip in z:
                    if "<b>Title reference" in snip or \
                       "<b>Title Reference" in snip or \
                        "<b>Guest" in snip or \
                        "<b>Recurring character" in snip or \
                        "<b>Note" in snip or \
                        "United States</td>" in snip or \
                        "<b>Trivia" in snip or \
                        "<b>Opening Credit" in snip or \
                        "<b>Special guest" in snip or \
                        "<b>Continuity Error" in snip or \
                        "<small>" in snip:
                        pass
                    else:
                        if  "<td class=" in snip:
                            f.write("<new episode>" + '\n\n')
                            snip = snip[snip.index(">")+1:]
                        snip = snip.replace("</td>","")
                        snip = snip.replace("<i>","")
                        snip = snip.replace("</i>","")
                        snip = snip.replace("<br/>","")
                        snip = snip.replace("</br>","")
                        snip = snip.replace("<hr/>","")
                        while "<span" in snip:
                            snip = snip[:snip.index("<span")] + \
                                   snip[snip.index("</span>")+7:]
                        while "<sup" in snip:
                            snip = snip[:snip.index("<sup")] + \
                                   snip[snip.index("</sup>")+6:]
                        if "<" in snip or ">" in snip:
                            print snip 
                        f.write(snip+'\n\n')
            f.close()

if __name__=='__main__':
	main()
