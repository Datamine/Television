# John Loeber | Oct 12 2014 | Debian Linux | Python 2.7.6

from os import listdir
from sys import argv

# takes two command-line arguments: (1) directory in which to analyze
# **sequentially numbered** files that are wikipedia episode summaries
# (2) dictionary file containing words and weights

with open(argv[2],"r") as b:
    dic = dict(map(lambda x: x.lower().rstrip('\n').split(" ")[::-1], b.readlines()))
dic = {x:float(y) for x,y in dic.items()}

def process(fi,g,FILTERSTOPWORDS):
    global dic
    if FILTERSTOPWORDS:
        global stopwords

    #format is [episode1,episode2,...] where episodex = [dict-words,total-words]
    eps = [[0,0]]
    with open(fi) as f:
        hits = {}
        for line in f:
            if line=="<new episode>\n":
                eps.append([0,0])
            elif line=="\n":
                pass
            else:
                x = line.replace(',','')
                x = x.replace('.','')
                x = x.replace('!','')
                x = x.replace('?','')
                x = x.replace('\'','')
                x = x.replace('"','')
                x = x.replace('\n','')
                x = x.replace('(','')
                x = x.replace(')','')
                new = x.split(" ")
                for word in new:
                    for j in dic:
                        # choose carefully between "j in word" and "j==word"
                        if j in word:
                            eps[-1][0] += dic[j]
                if FILTERSTOPWORDS:
                    eps[-1][1]+= len([z for z in new if z not in stopwords])
                else:
                    eps[-1][1]+= len(new)
    if eps[0]==[0,0]:
        del eps[0]
    for i in eps:
        if i==[0,0]:
            g.write(str(i[0])+", "+str(i[1])+" 0.0"+"\n")
        else:
            g.write(str(i[0])+", "+str(i[1])+", "+str(i[0]/float(i[1]))+"\n")
    g.write('\n')
    return

def main():
    if argv[3].lower()=="y":
        FILTERSTOPWORDS = True
    elif argv[3].lower()=="n":
        FILTERSTOPWORDS = False
    else:
        raise Exception("Erroneous command-line arg. Need 'y' or 'n' to filter"
                        " or not filter stopwords, respectively.")
    if FILTERSTOPWORDS:
        global stopwords
        with open("stopwords-final","r") as h:
            stopwords = filter(lambda y: y!='',[x.replace('\n','') 
                               for x in h.readlines()])
    folder = argv[1]
    files = listdir(folder)
    files.sort()
    files = [folder+x for x in files]
    g = open(folder[:-1]+"-analyzed","w")
    for index, f in enumerate(files):
        # uncomment this line if you like more explicit separation between docs
        #g.write("document " + str(index))
        g.write('\n')
        process(f,g,FILTERSTOPWORDS)
    g.close()

if __name__=='__main__':
    main()
