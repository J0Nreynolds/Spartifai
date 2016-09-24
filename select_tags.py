from clarifai.client import ClarifaiApi
import nltk
import pdb
from collections import Counter
from collections import defaultdict
import subprocess

def say(string):
    subprocess.call(['say', string])

def main():
    clarifai_api = ClarifaiApi()
    image_array = [open('output/rgb_img_' + str(x) + ".jpg", 'rb') for x in xrange(1,13)]
    results_json = clarifai_api.tag(image_array, select_classes = "animal,car,road,police")
    for x in xrange(len(results_json['results'])):
        results = results_json['results'][x]
        result =results['result']
        tag = result['tag']
        classes = tag['classes']
        probs = tag['probs']
        for x in xrange(len(probs)):
            if probs[x] >= .85:
                say("Watch out, there is a " + str(classes[x]) + " in front of you")

main()
