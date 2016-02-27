from clarifai.client import ClarifaiApi
clarifai_api = ClarifaiApi()

results_json = clarifai_api.tag_images([open('Captures/capture1.png', 'rb'), open('Captures/capture2.png', 'rb'), open('Captures/capture3.png', 'rb'), open('Captures/capture4.png', 'rb'), open('Captures/capture5.png', 'rb'), open('Captures/capture6.png', 'rb'), open('Captures/capture7.png', 'rb'), open('Captures/capture8.png', 'rb'), open('Captures/capture9.png', 'rb'), open('Captures/capture10.png', 'rb')])
results = results_json['results']
print results