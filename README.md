# Autonomous Self-driving Car in GTA-5 #
## Demo ##
### Driving on the Highway ###
![gif](Demo/demo1.gif)
### Driving in the City ###
![gif](Demo/demo2.gif)

Note: This AI is trained on the highway, but still performs relatively well in the city.
## About ##
The goal of this project is to build a self-driving car with deep learning and computer vision, which can navigate in different environments. The project is inspired by the work done by Sentdex. After experimenting with different convolutional neural networks, NVIDIA's PilotNet is chosen due to its faster prediction rate. YOLOv3, one of the most popular object detection algorithm, is also integrated with PilotNet to add steering, throttle, and brake control as per traffic density.
Detailed Explaination: https://medium.com/@alzaibnasiruddin/building-a-self-driving-vehicle-in-gta-v-using-deep-learning-and-convolutional-neural-network-696b38b4c81e
## Setup and Requirements ##
1. Grand Theft Auto-5 (turn on hood camera)
2. Python 3.6
3. Tensorflow
4. Keras
5. OpenCV
6. Numpy
7. Pygame
8. Xbox 360 Emulator(https://www.x360ce.com/)
9. vJoy (http://vjoystick.sourceforge.net/site/)

## Dataset ##
### My Dataset ###
100,000 images with respective steering angle and throttle is collected by driving the car on the highway. However, only 39,046 images are left after balancing the data, therefore the dataset is artificially expanded by flipping the image along the horizontal axis, and multiplying the steering angle by -1. 
#### Steering ####
![alt text](Demo/steering.JPG)
#### Throttle ####
![alt text](Demo/throttle.JPG)


[Original dataset with 100,000 images used to trained this model can be found here](https://drive.google.com/drive/folders/1R787vkWaMe5nsWyLpbXTG55aUv4YteTo?usp=sharing)
### Custom Dataset ###
Use collect_data.py to generate your custom dataset. Ensure the GTA-5 window size same as in the collect_data.py
Upload the collected data on Google Drive to train your model on Google Colab. 
## Training (Google Colab) ##
[Training code can be found here](https://github.com/Alzaib/Autonomous-Self-Driving-Car-GTA-5/blob/master/training_colab/GTA_5_steering.ipynb)
1. Upload the training data on Google Drive
2. Create a Google Colab project, ensure GPU is enabled
3. Upload the .ipynb file under training_colab to Google Colab
4. Run the code

[Trained model, and YOLOv3 weights can be found here](https://drive.google.com/drive/folders/1laagsAkn_TqjyKw1zvd5Okct5Sd3WONF?usp=sharing)
## Usage ## 
1. Download and add Xbox 360 Emulator where GTA is installed
2. Install vJoy
3. Set vJoy in Xbox 360 Emulator
4. Download or clone this repo
5. Run test_model_steer.py
## Future Improvements ##
1. Collect diverse dataset
2. Increase resolution of the images in the dataset
3. Use CNN+LSTM to train the model
## Acknowledgement ##
Sentdex: https://www.youtube.com/playlist?list=PLQVvvaa0QuDeETZEOy4VdocT7TOjfSA8a

Pysource: https://www.youtube.com/watch?v=h56M5iUVgGs&t=11s
