# John Loeber | Nov-03-2014 | Python 2.7.6 | Debian Linux | www.johnloeber.com

from sys import argv

# For filtering the results of allresults.py to weighted representations by year
# Takes one command-line arg: name of the allresults.py output file

textin = argv[1]
with open(textin,"r") as g:
    x = g.readlines()
x = [a for a in x if "}" not in a and " " not in a]
x = filter(lambda y: y!="\n",x)
z = range(1950,2015)
with open("results_"+textin, "w") as f:
    for i in zip(z,x):
        f.write(str(i[0]) + ", " + i[1])
