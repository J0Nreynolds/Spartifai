

from clarifai.client import ClarifaiApi
import nltk
import pdb
from collections import Counter
from collections import defaultdict
import subprocess

def main():
    clarifai_api = ClarifaiApi()
    image_array = [open('Captures/Capture' + str(x) + ".png") for x in xrange (1,10)]
    results_json = clarifai_api.tag(image_array, select_classes = "animal,car,road,police")
    for x in xrange(len(results_json['results'])):
        results = results_json['results'][x]
        result =results['result']
        tag = result['tag']
        classes = tag['classes']
        probs = tag['probs']
        for x in xrange(len(probs)):
            if probs[x] >= .2:
                print "Watch out, there is a " + classes[x] + " in front of you"

main()
