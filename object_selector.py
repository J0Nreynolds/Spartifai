from clarifai.client import ClarifaiApi
import pdb
from collections import Counter
from collections import defaultdict
import subprocess
import operator

def createHashmap(results):
    for x in xrange(0,len(results)):
        resultsData = {}
        for y in range(0, len(results[x]['result']['tag']['probs'])):
            resultsData[str(results[x]['result']['tag']['classes'][y])] = results[x]['result']['tag']['probs'][y]
        result = sorted(resultsData.items(), key=operator.itemgetter(1))[::-1]
        print result
        print "\n"
        relevantData.append(result)
    #print relevantData

def main():
    clarifai_api = ClarifaiApi()

    #ADD ANY MORE IMAGES HERE, PROGRAM SHOULD ADJUST
    image_array = [open('output/rgb_img_' + str(x) + ".jpg", 'rb') for x in xrange(1,13)]
    results_json = clarifai_api.tag_images(image_array)
    results = results_json['results']
    createHashmap(results)

    find_objects()
    text_results_string = str(namesOfObjects)
    say(text_results_string)

def say(string):
    subprocess.call(['say', string])

def find_objects():
    del prominentObjects[:]
    del namesOfObjects[:]
    del names[:]
    for x in xrange(0 , len(relevantData)-1):
        highestInfo = find_highest(x)
        prominentObjects.append(highestInfo)

    isDone = checkForPopular()

    while(isDone == False):
        find_objects()
    pass

def checkForPopular():
    D = defaultdict(list)
    for i,item in enumerate(names):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}

    if len(D)!=0 and len(D.values())>2:
        print D
        for x in xrange(0, len(D)):
            indices = D.itervalues().next()
            for index in indices:
                del relevantData[index][0]
        return False
    else:
        return True

def find_highest(x):
    hourRatio = ((2.0*x + 1.0)/2.0)/len(relevantData)
    timeInHours = put_time_in_hours(hourRatio)
    highestInfo = []
    effectiveprobs = [a[1] for a in relevantData[x]] +  [a[1] for a in relevantData[x+1]]
    effectivenames = [a[0] for a in relevantData[x]] + [a[0] for a in relevantData[x+1]]
    adjustedprobs = adjust_probs(effectiveprobs)

    duplicate_pairs = find_duplicates(effectivenames)
    adjustedprobs = add_duplicate_probs(duplicate_pairs, adjustedprobs)

    indexOfHighest = find_most_likely(adjustedprobs)

    highestInfo.append(effectivenames[indexOfHighest])
    highestInfo.append(effectiveprobs[indexOfHighest])

    names.append(str(effectivenames[indexOfHighest]))
    namesOfObjects.append(str(effectivenames[indexOfHighest]) + " at " + str(int(timeInHours)) + " o'clock.")

    return highestInfo

def put_time_in_hours(hourRatio):
    hours = round(hourRatio*6, 0)
    adjustedhours = 0
    if hours>3 :
        adjustedhours = hours - 3
    else :
        adjustedhours = hours + 9
    return adjustedhours

def find_most_likely(adjustedprobs):
    index = 0
    for x in xrange(0, len(adjustedprobs)):
        if adjustedprobs[index] < adjustedprobs[x]:
            index = x
    return index

def adjust_probs(effectiveprobs):
    for x in xrange(0,len(effectiveprobs)):
        effectiveprobs[x] -= .85
    return effectiveprobs

def find_duplicates(effectiveids):
    D = defaultdict(list)
    for i,item in enumerate(effectiveids):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}
    return D

def add_duplicate_probs(duplicate_pairs, adjustedprobs):
    for x in xrange(0,len(duplicate_pairs)):
        duplicate_pair = duplicate_pairs.itervalues().next()
        index0 = duplicate_pair[0]
        index1 = duplicate_pair[1]
        adjustedprobs[index0] += adjustedprobs[index1]
        adjustedprobs[index1] = 0
    return adjustedprobs

relevantData = []
prominentObjects = []
namesOfObjects = []
names = []

main()
