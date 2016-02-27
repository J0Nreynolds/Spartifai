from clarifai.client import ClarifaiApi
import nltk
import pdb

def return_nouns(result):
    words = result['result']['tag']['classes']
    tagged = nltk.pos_tag(words)
    parse_tagged(tagged)

clarifai_api = ClarifaiApi()

results_json = clarifai_api.tag_images([open('Captures/capture1.png', 'rb'), open('Captures/capture2.png', 'rb'), open('Captures/capture3.png', 'rb'), open('Captures/capture4.png', 'rb'), open('Captures/capture5.png', 'rb'), open('Captures/capture6.png', 'rb'), open('Captures/capture7.png', 'rb'), open('Captures/capture8.png', 'rb'), open('Captures/capture9.png', 'rb'), open('Captures/capture10.png', 'rb')])
results = results_json['results']

for result in results:
    return_nouns(result)