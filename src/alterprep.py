positions = []
def map(sublist, maplist):
    temp = []
    assert(len(sublist) == len(maplist))
    for k,v, in enumerate(sublist):
        temp.append(v + maplist[k])
    return temp
        
with open('positions.txt', 'r') as f:
    for line in f:
        positions.append([float(x) for x in line.strip('\n').split(':')])
alteredpositions = []


for k,v in enumerate(positions[::-1]):
    alteredpositions.append(map(v,[0,41,0]))

with open('position2.txt', 'w') as f:
    for k,v in enumerate(positions):
        tempstring = ""
        for v2 in v:
            tempstring += str(v2) + ":"
        f.write(tempstring + '\n')
    for k,v in enumerate(alteredpositions[:-12]):
        tempstring = ""
        for v2 in v:
            tempstring += str(v2) + ":"
        f.write(tempstring + '\n')

