from clarifai.client import ClarifaiApi
import nltk
import pdb
from collections import Counter
from collections import defaultdict
import subprocess

def main():
    clarifai_api = ClarifaiApi()
    file = clarifai_api.tag_images(open("Captures/Capture3.png"), select_classes = "animal,person,computer")
    print file

main()
