from clarifai.client import ClarifaiApi
import pdb
from collections import Counter
from collections import defaultdict
import subprocess

def createHashmap(results):
    relevantData = []
    for x in xrange(0,len(results)):
        resultsData = {}
        for y in range(0, len(results[x]['result']['tag']['probs'])):
            resultsData[str(results[x]['result']['tag']['classes'][y])] = results[x]['result']['tag']['probs'][y]
        relevantData.append(resultsData)
    print relevantData
    return relevantData

def main():
    clarifai_api = ClarifaiApi()

    #ADD ANY MORE IMAGES HERE, PROGRAM SHOULD ADJUST
    image_array = [open('output/rgb_img_' + str(x) + ".jpg", 'rb') for x in xrange(1,13)]
    results_json = clarifai_api.tag_images(image_array)
    results = results_json['results']
    relevantData = createHashmap(results)

    find_objects(relevantData)
    text_results_string = str(namesOfObjects)
    espeak(text_results_string)

def espeak(string):
    print string
    subprocess.call(['espeak', "-s", "100", "-v", "+f2", string])

def find_objects(relevantData):
    del prominentObjects[:]
    del namesOfObjects[:]
    del names[:]
    for x in xrange(0 , len(relevantData)-1):
        highestInfo = find_highest(x, relevantData)
        prominentObjects.append(highestInfo)
    
    relevantData, isDone = checkForPopular(relevantData)

    while(isDone == False):
        find_objects(relevantData)

def checkForPopular(relevantData):
    D = defaultdict(list)
    for i,item in enumerate(names):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}

    if len(D)!=0 :
        print D
        for x in xrange(0, len(D)):
            indices = D.itervalues().next()
            for index in indices:
                del relevantData[index][relevantData[index].keys()[0]]
        return relevantData, False
    else:
        return relevantData, True

def find_highest(x, relevantData):
    hourRatio = ((2.0*x + 1.0)/2.0)/len(relevantData)
    timeInHours = put_time_in_hours(hourRatio)
    highestInfo = []
    effectiveprobs = relevantData[x].values() + relevantData[x+1].values()
    effectivenames = relevantData[x].keys() + relevantData[x+1].keys()
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

prominentObjects = []
namesOfObjects = []
names = []

main()

