import re

filename = './WWW_aeasy03380867.dat' # Should parameterize this
outfilename = './newresults.csv' # Also parameterize this
prefix = 'N6E01' # Should also figure out what this is and make a real variable of it.

with open(filename) as fin:
    inlines = [line.strip() for line in fin.readlines()]

dates = []
realdata = {}

DTTokenString = prefix + '(?P<year>\d\d)(?P<month>\d\d)(?P<day>\d\d)(?P<var1>.)(?P<hour>\d\d)(?P<var2>.*)'
inforegex = re.compile(DTTokenString)

for line in inlines:
    tokens = line.split()
    # ignore first token, grab broad datetime info from second token, remaining tokens are data at minute intervals
    lineinfo = inforegex.match(tokens[1]).group
    dtlinestring = '20{}-{}-{}T{}:'.format(lineinfo('year'),lineinfo('month'),lineinfo('day'),lineinfo('hour'))
    varstr = '{}_{}'.format(lineinfo('var1'),lineinfo('var2'))
    if (varstr not in realdata.keys()):
        realdata[varstr] = {}
    if (dtlinestring not in realdata[varstr].keys()):
        realdata[varstr][dtlinestring] = []
    for dat in tokens[2:]:
        realdata[varstr][dtlinestring].append(dat)
    dates.append(dtlinestring)

dates = list(set(dates))
dates.sort()

outlines = []
current = ['"datetime"']
for key in realdata.keys():
    current.append('"{}"'.format(key))

outlines.append((','.join(current))+'\n')

for curdate in dates:
    for m in range(60):
        current = ['"{}{:02d}"'.format(curdate,m)]
        for key in realdata.keys():
            try:
                val = realdata[key][curdate][m]
            except:
                val = ''
            current.append('"{}"'.format(val))
        outlines.append((','.join(current))+'\n')

with open(outfilename, 'wt') as outFile:
    outFile.writelines(outlines)
