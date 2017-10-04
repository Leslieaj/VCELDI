#import os

with open('../example9result.txt', 'r') as reader:
    counter = 0
    findex = 1
    replaceindex = 0
    next(reader)
    for line in reader:
        if counter==0:
            writer = open('example9result'+str(findex)+'.txt', 'w+')
            writer.truncate()
            print >> writer, 'rlset r$\n'.strip()
        if (counter-2) % 4 == 0 or counter == 2:
            line = line.replace('example9result','example9result'+str(findex))
        print >> writer, line.strip()
        counter += 1
        replaceindex += 1
        if counter >= 8000:
            print >> writer, 'showtime;'.strip()
            writer.close()
            counter = 0
            findex += 1
