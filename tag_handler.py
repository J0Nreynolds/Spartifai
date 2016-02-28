from clarifai.client import ClarifaiApi
import say
import pdb
from collections import Counter
from collections import defaultdict
import operator
import random

GENERALITIES_PHRASE = "In general, the following elements are in your vicinity... "
SPECIFICS_SWITCHES = ['you will find', 'there is', 'you might encounter']
SPECIFICS_PHRASE = "At your %s-o-clock, %s %s"
REMOVALS = ['facial expression', 'blur', 'business', 'no person']

def createHashmap(results):
    relevantData = []
    for x in xrange(0,len(results)):
        resultsData = {}
        for y in range(0, len(results[x]['result']['tag']['probs'])):
            resultsData[str(results[x]['result']['tag']['classes'][y])] = results[x]['result']['tag']['probs'][y]
        result = sorted(resultsData.items(), key=operator.itemgetter(1))[::-1]
        # print result
        # print "\n"
        relevantData.append(result)
    #print relevantData
    return relevantData

NUM_GENERALITIES = 5
def find_generalities(results):
    generalities = []
    counts = {}
    for result in results:
        for a in result:
            if a[0] not in counts:
                counts[a[0]] = 1
            else:
                counts[a[0]] += 1

    for key in counts:
        if key in REMOVALS:
            for x in xrange(len(results)):
                results[x] = [a for a in results[x] if a[0] != key]

    for x in xrange(NUM_GENERALITIES):
        common = max(counts.iteritems(), key=operator.itemgetter(1))[0]
        generalities.append(common)
        del counts[common]
        for x in xrange(len(results)):
            results[x] = [a for a in results[x] if a[0] != common]

    for key in counts:
        if counts[key] >= float(2)*float(len(results))/float(3):
            for x in xrange(len(results)):
                results[x] = [a for a in results[x] if a[0] != key]
    return generalities


WINDOW_SIZE = 2
def find_specifics(results):
    windows = []
    for x in xrange(len(results)/WINDOW_SIZE):
        combined = {}
        for y in xrange(WINDOW_SIZE):
            result = results[WINDOW_SIZE * x + y]
            for tag in result:
                if tag[0] not in combined:
                    combined[tag[0]] = tag[1]
                else:
                    combined[tag[0]] = (combined[tag[0]] + tag[1])/2
        maximum_in_window = max(combined.iteritems(), key=operator.itemgetter(1))[0]
        windows.append(maximum_in_window)
    return windows

def main(path):
    clarifai_api = ClarifaiApi()

    #ADD ANY MORE IMAGES HERE, PROGRAM SHOULD ADJUST
    image_array = [open(path+ '/output/rgb_img_' + str(x) + ".jpg", 'rb') for x in xrange(1,13)]
    results_json = clarifai_api.tag_images(image_array)
    results = createHashmap(results_json['results'])
    generalities = find_generalities(results)
    print generalities
    generalities_phrase = GENERALITIES_PHRASE
    for x in xrange(len(generalities)):
        if x == len(generalities_phrase)-1:
            generalities_phrase += 'and ' + generalities[x] + ' .'
        else:
            generalities_phrase += generalities[x] + ', '
    specifics = find_specifics(results)
    print specifics
    say.say(generalities_phrase)
    for x in xrange(len(specifics)):
        hour = put_time_in_hours(float(x)/float(len(specifics)))
        choice = random.choice(SPECIFICS_SWITCHES)
        specifics_phrase = SPECIFICS_PHRASE % (int(hour), choice, specifics[x])
        say.say(specifics_phrase)


# #iterates trhough relevantData to get our data output
# def find_objects():
#     del prominentObjects[:]
#     del namesOfObjects[:]
#     del names[:]
#     for x in xrange(0 , len(relevantData)-1):
#         highestInfo = find_highest(x)
#         prominentObjects.append(highestInfo)
#
#     isDone = checkForPopular()
#
#     while(isDone == False):
#         find_objects()
#     pass


#this is the function that actually collects all the data (iterated over in find object), by analyzing image overlap
# def find_highest(x):
#     hourRatio = ((2.0*x + 1.0)/2.0)/len(relevantData)
#     timeInHours = put_time_in_hours(hourRatio)
#     highestInfo = []
#     effectiveprobs = [a[1] for a in relevantData[x]] +  [a[1] for a in relevantData[x+1]]
#     effectivenames = [a[0] for a in relevantData[x]] + [a[0] for a in relevantData[x+1]]
#     adjustedprobs = adjust_probs(effectiveprobs)
#
#     duplicate_pairs = find_duplicates(effectivenames)
#     adjustedprobs = add_duplicate_probs(duplicate_pairs, adjustedprobs)
#
#     indexOfHighest = find_most_likely(adjustedprobs)
#
#     highestInfo.append(effectivenames[indexOfHighest])
#     highestInfo.append(effectiveprobs[indexOfHighest])
#
#     names.append(str(effectivenames[indexOfHighest]))
#     namesOfObjects.append(str(effectivenames[indexOfHighest]) + " at " + str(int(timeInHours)) + " o'clock.")

    # return highestInfo
#convert degree ratio to hours
def put_time_in_hours(hourRatio):
    hours = round(hourRatio*6, 0)
    adjustedhours = 0
    if hours>3 :
        adjustedhours = hours - 3
    else :
        adjustedhours = hours + 9
    return adjustedhours
#finds the highest prob. object
def find_most_likely(adjustedprobs):
    index = 0
    for x in xrange(0, len(adjustedprobs)):
        if adjustedprobs[index] < adjustedprobs[x]:
            index = x
    return index

# #lowers the impact of repeat
# def adjust_probs(effectiveprobs):
#     for x in xrange(0,len(effectiveprobs)):
#         effectiveprobs[x] -= .85
#     return effectiveprobs
# #finds the duplicate key: value pairs once two image results are merged
# def find_duplicates(effectiveids):
#     D = defaultdict(list)
#     for i,item in enumerate(effectiveids):
#         D[item].append(i)
#     D = {k:v for k,v in D.items() if len(v)>1}
#     return D
# #adds together two duplicate key-value pairs
# def add_duplicate_probs(duplicate_pairs, adjustedprobs):
#     for x in xrange(0,len(duplicate_pairs)):
#         duplicate_pair = duplicate_pairs.itervalues().next()
#         index0 = duplicate_pair[0]
#         index1 = duplicate_pair[1]
#         adjustedprobs[index0] += adjustedprobs[index1]
#         adjustedprobs[index1] = 0
#     return adjustedprobs
