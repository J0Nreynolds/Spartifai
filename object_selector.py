from clarifai.client import ClarifaiApi
import nltk
import pdb
from collections import Counter
from collections import defaultdict

def return_nouns(result):
    words = result['result']['tag']['classes']
    tagged = nltk.pos_tag(words)
    non_nouns = parse_tagged(tagged)
    for index, non_noun in enumerate(non_nouns): 
        result['result']['tag']['concept_ids'].pop(non_noun-index)
        result['result']['tag']['classes'].pop(non_noun-index)
        result['result']['tag']['probs'].pop(non_noun-index)
    return result

def parse_tagged(tagged): 
    non_nouns = []
    for index, pair in enumerate(tagged):
        if 'NN' not in pair:
            non_nouns.append(index)
    return non_nouns

def find_objects(results):
    for x in xrange(0 , len(results)-2):
    effectiveids = results[x]['result']['tag']['concept_ids'] + results[x+1]['result']['tag']['concept_ids']
    effectiveprobs = results[x]['result']['tag']['probs'] + results[x+1]['result']['tag']['probs']

    duplicate_pairs = find_duplicates(effectiveids)
    add_duplicate_probs(duplicate_pairs, effectiveprobs)

def find_duplicates(effectiveids):
    D = defaultdict(list)
    for i,item in enumerate(effectiveids):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}
    pdb.set_trace()
    return D

def add_duplicate_probs(duplicate_pairs, effectiveprobs):
    for x in xrange(0,len(duplicate_pairs)-1):
        duplicate_pair = duplicate_pairs.itervalues().next()
        index0 = duplicate_pair[0]
        index1 = duplicate_pair[1]


clarifai_api = ClarifaiApi()

image_array = [open('Captures/capture1.png', 'rb'), open('Captures/capture2.png', 'rb'), open('Captures/capture3.png', 'rb'), open('Captures/capture4.png', 'rb'), open('Captures/capture5.png', 'rb'), open('Captures/capture6.png', 'rb'), open('Captures/capture7.png', 'rb'), open('Captures/capture8.png', 'rb'), open('Captures/capture9.png', 'rb'), open('Captures/capture10.png', 'rb')]
results_json = clarifai_api.tag_images(image_array)
results = results_json['results']

for result in results:
    result = return_nouns(result)

print results

find_objects(results)
