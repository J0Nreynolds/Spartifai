from clarifai.client import ClarifaiApi
import nltk
import pdb
from collections import Counter
from collections import defaultdict
import subprocess

def main():
    clarifai_api = ClarifaiApi()

    #ADD ANY MORE IMAGES HERE, PROGRAM SHOULD ADJUST
    image_array = [open('Captures/capture1.png', 'rb'), open('Captures/capture2.png', 'rb'), open('Captures/capture3.png', 'rb'), open('Captures/capture4.png', 'rb'), open('Captures/capture5.png', 'rb'), open('Captures/capture6.png', 'rb'), open('Captures/capture7.png', 'rb'), open('Captures/capture8.png', 'rb'), open('Captures/capture9.png', 'rb'), open('Captures/capture10.png', 'rb')]
    results_json = clarifai_api.tag_images(image_array)
    results = results_json['results']
    print "GAY GAY GAY"*1000

    # for result in results:
    #     result = return_nouns(result)
    print "FUCK FUCK FUCK"*1000

    all_results, text_results = find_objects(results)
    text_results_string = str(text_results)
    espeak(text_results_string)

def espeak(string):
    subprocess.call(['espeak', "-s", "100", "-v", "+f2", string])

# def return_nouns(result):
#     words = result['result']['tag']['classes']
#     tagged = nltk.pos_tag(words)
#     non_nouns = parse_tagged(tagged)
#     for index, non_noun in enumerate(non_nouns): 
#         result['result']['tag']['concept_ids'].pop(non_noun-index)
#         result['result']['tag']['classes'].pop(non_noun-index)
#         result['result']['tag']['probs'].pop(non_noun-index)
#     return result

# def parse_tagged(tagged): 
#     non_nouns = []
#     for index, pair in enumerate(tagged):
#         if 'NN' not in pair:
#             non_nouns.append(index)
#     return non_nouns

def find_objects(results):
    prominentObjects = []
    namesOfObjects = []
    for x in xrange(0 , len(results)-1):
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
        namesOfObjects.append(str(effectivenames[indexOfHighest]) + " at " + str(int(timeInHours)) + " o'clock.")
        highestInfo.append(effectiveprobs[indexOfHighest])

        prominentObjects.append(highestInfo)
    return prominentObjects, namesOfObjects

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

main()

