from clarifai.client import ClarifaiApi
import nltk
import pdb
from collections import Counter
from collections import defaultdict
import subprocess

def main():
    clarifai_api = ClarifaiApi()

    image_array = [open('output/rgb_img_' + str(x) + ".jpg", 'rb') for x in xrange(1,13)]
    results_json = clarifai_api.tag_images(image_array)
    results = results_json['results']
    return results

def espeak(string):
    print string
    subprocess.call(['espeak', "-s", "100", "-v", "+f2", string])

def find_objects(results):
    print results
    for x in xrange(0 , len(results)-1):
        highestInfo = get_information(x)
        prominentObjects.append(highestInfo)
    return namesOfObjects, names

def get_information(x):
    hourRatio = ((2.0*x + 1.0)/2.0)/len(results) 
    timeInHours = put_time_in_hours(hourRatio)
    highestInfo = []
    effectiveids = results[x]['result']['tag']['concept_ids'] + results[x+1]['result']['tag']['concept_ids']
    effectiveprobs = results[x]['result']['tag']['probs'] + results[x+1]['result']['tag']['probs']
    effectivenames = results[x]['result']['tag']['classes'] + results[x+1]['result']['tag']['classes']
    adjustedprobs = adjust_probs(effectiveprobs)

    duplicate_pairs = find_duplicates(effectiveids)
    adjustedprobs = add_duplicate_probs(duplicate_pairs, adjustedprobs)

    indexOfHighest = find_most_likely(adjustedprobs)
    highestInfo.append(effectiveids[indexOfHighest])
    highestInfo.append(effectivenames[indexOfHighest])
    names.append(str(effectivenames[indexOfHighest]))
    namesOfObjects.append(str(effectivenames[indexOfHighest]) + " at " + str(int(timeInHours)) + " o'clock.")
    highestInfo.append(effectiveprobs[indexOfHighest])

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

def check_room_qualities(prominentObjects, text_results, names, results):
    D = defaultdict(list)
    for i,item in enumerate(names):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}
    a = 0

    for x in xrange(0,len(D)):
        indices = D.itervalues().next()
        if len(indices) > 2:
            for index in indices:
                key = D.keys()[0]
                unicode_key = unicode(key, "utf-8")
                this_index = results[index]['result']['tag']['classes'].index(unicode_key)
                results[this_index]['result']['tag']['concept_ids'].pop(0)
                results[this_index]['result']['tag']['classes'].pop(0)
                results[this_index]['result']['tag']['probs'].pop(0)

                prominentObjects.pop(index-a)
                text_results.pop(index-a)
                prominentObjects.insert(index-a, get_information(this_index))
                a += 1
    text_results, names = find_objects(results)

prominentObjects = []
namesOfObjects = []
names = []
results = main()
text_results, names = find_objects(results)
check_room_qualities(prominentObjects, text_results, names, results)
text_results_string = str(text_results)
espeak(text_results_string)
