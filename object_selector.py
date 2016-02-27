from clarifai.client import ClarifaiApi
import nltk
import pdb

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
    print(non_nouns)
    return non_nouns

clarifai_api = ClarifaiApi()

results_json = clarifai_api.tag_images([open('Captures/capture1.png', 'rb'), open('Captures/capture2.png', 'rb'), open('Captures/capture3.png', 'rb'), open('Captures/capture4.png', 'rb'), open('Captures/capture5.png', 'rb'), open('Captures/capture6.png', 'rb'), open('Captures/capture7.png', 'rb'), open('Captures/capture8.png', 'rb'), open('Captures/capture9.png', 'rb'), open('Captures/capture10.png', 'rb')])
results = results_json['results']

for result in results:
    result = return_nouns(result)

print results