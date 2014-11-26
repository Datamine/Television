# John Loeber | Oct 24 2014 | Debian Linux | Python 2.7.6 | www.johnloeber.com

from sys import argv
from os import listdir
from collections import Counter
from ast import literal_eval

# takes two command-line args:
# 1. Dictionary for which to report word frequency per file
# 2. Directory where year-labelled files (e.g. "1975","2010") are located

def main():
    with open(argv[1],"r") as f:
        dic = dict(map(lambda x: x.lower().rstrip('\n').split(" ")[::-1], f.readlines()))
    path = listdir(argv[2])
    path.sort()
    path = filter(lambda x: x.isdigit(),path)
    with open(argv[1]+"_"+argv[2].rstrip('/'), "w") as h:
        for i in path:
            hits = {}
            # for verification/debugging
            # print i
            with open(argv[2]+i,'r') as g:
                gf = g.read().split('\n')
            dd = literal_eval(gf[0])
            dsum = float(gf[1])
            for j in dic:
                 for s in dd:
                    # choose carefully between "if j in s" (substring)
                    # "if j==s" (string equality)
                    if j in s:
                        # for verification/debugging
                        # print s, dd[s]
                        if j in hits:
                            hits[j] += float(dic[j]) * dd[s]
                        else:
                            hits[j] = float(dic[j])*dd[s]
            allhits = sum(hits.values())
            h.write(str(hits)+'\n'+i+" "+str(allhits)+'\n'+str(allhits/dsum)+'\n\n')

if __name__=='__main__':
    main()
