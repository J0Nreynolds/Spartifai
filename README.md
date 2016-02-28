#Spartify

## Inspiration
When introduced to the Clarifai API, our first thought was to use it to provide vision where it currently isn't available, and to nobody is it a bigger problem than it is to the blind community. Seeing-eye dogs are undeniably powerful tools at their disposal, but if a technology were created in the future to help them fully analyze their environment, it could change their quality of life drastically. From here, we set off to creating our prototype. 

## What it does
Using a Kinect sensor which feeds data to the Clarifai API, our application is able to discern objects in your surroundings in a 180 degree radius. It then uses a text to speech program to read this data out loud, giving a blind person a general understanding of their environment. 

## How we built it
On the software end, we used Python in conjunction with the Clarifai API to process images and provide the user with a general understanding of the positions of certain objects. On the hardware end, we used an Arduino 101 Intel Curie Board in conjunction with a rotary sensor and a grove base shield to determine the angles at which photos were taken by our Kinect sensor and to feed the pictures to our Python application. Lastly, we used Kinect's depth perception abilities to perform some preliminary distance calculations, to help a blind person avoid obstacles. 

## Challenges we ran into
1. Figuring out what hardware to use-- on multiple occasions we ran into hardware limitations due to a lack of equipment. 
2. Exporting Arduino outputs into python.
3. Acquiring accurate data from the rotary sensor.

## Accomplishments that we're proud of
1. The makeshift mechanical construction we created in order to hold our hardware.
2. Our output is fairly detailed, providing an overview of the general environment as well as specific directional information.
3. Our integration of the Clarifai API and our utilization of the data provided to provide information to the user.

## What we learned
1. The abilities and possible utilizations of the Clarifai API.
2. We were able to construct a mechanical alternative to the hardware we were unable to acquire.
3. We learned a lot about Python and its computing power.

## What's next for Spartifai
In the future, we would look to scaling down the size of our prototype so it would be better suited to a blind person. One idea we have is to create a device that clips on to sunglasses, much like the ones many blind people wear today.


SpartaHack 2016 Hack with Clarifai API
