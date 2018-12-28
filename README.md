# airs - Aerial Images Road Segmentation

## Problem
Road segmentation is detecting roads in aerial images usually taken by satellites. Specifically, given an aerial image, it is required to output a binary mask for the input image showing for each pixel if it belongs to a road or not.

## Solution
A per-pixel-classification technique is used to build the output binary mask, that is, each pixel is independently classified as a part of a road or not.

To classify pixel (x, y), the pixels contained in the surrounding window of a predefined side length 'L' centered at (x, y) will be used as features, so that the input features vector will contain the (r, g, b) values of all these pixels (including the current target pixel at (x, y)), which makes the features vector size = 3xLxL.

As a classifier, a deep neural network of multiple hidden layers is used. The output layer consists of two neurons representing the two output classes in one-hot vector representation.

## Implementation
The described solution is implemented in python using Tensorflow machine learning library (version 1.1.0), and pillow (version 4.1.0). It consists of four separate python scripts with the following purposes:
- Converting the image data set into three csv text files, train.csv, test.csv and valid.csv used for training, testing and validation respectively.
- Building a classifier, training it using the generated training and testing csv text file, and saving it in a Tensorflow format.
- Loading an already trained classifier, and calculate its accuracy using the generating validation csv text files.
- Classifying an input image.

The first step is converting the image data set into csv data files that can be fed into the classifier for training, testing and validation. The images are divided into training images, testing images and validation images in a predefined directory structure, these directories are scanned by the first script mentioned above.

To obtain good results, the ratio between the samples of the two classes shouldn't be too large, and naturally the ratio between non-road pixels and road pixels in an image is very large, that's why dropout must be performed to balance the dataset, but it must be performed in a random fashion to ensure that the classifier is exposed to a diverse set of samples from each class. To perform the dropout for each image, the script loads the image along with its corresponding expected output, then it divides it into two sets of pixels, road pixels and non-road pixels, randomly shuffles both sets, and then for each road pixel, we take two non-road pixels (which ensures the ratio between road samples and non-road samples to be 1:2 in the output csv file), generate their feature vectors as mention earlier, and write them to the output file. This is done for training images, testing images and validation images to generate the three files.

The second step is training the classifier. The second script uses Tensorflow to initialize a deep neural network of four hidden layers of sizes 100, 150, 100, 50 neurons respectively, then loads the training and testing csv files, and use it to train the neural network for a predefined number of iterations, the testing data is used to evaluate the accuracy of the model at the end of the training. After the training finishes, the script saves the model on the file system in a Tensorflow specific format that can be loaded to recalculate its accuracy, or use it in classifying input images.

The third script is used to test the model accuracy, it loads the model and the test csv file, and calculate the accuracy.

Classification of an input image is done using the fourth script, it takes the names of the input and output image names as command line arguments, it loads the model and the input image from the 'image-input' directory, generate the feature vector for each pixel, classify it using the loaded classifier, and generate the output image with zero/one value for each pixel based on the classifier prediction for that pixel, then it saves the generated image in 'image-output' directory using the output image name entered in the command line arguments.

## CSV file format
In the current implmentation the window size is 5 pixels.

The csv files follow a very simple format:
- each record (line) is a single feature vector with its ground truth outcome.
- each feature vector consists of the RGB values of pixels contained in a 5x5 window (three integers for each pixel), and a binary value representing the class of the central pixel of that window.

Accordingly, each line in the csv files should consist of (3x5x5) + 1 integers as follows:
```
r1, g1, b1, r2, g2, b2, r3, g3, b3, . . . . . , r25, g25, b25, y
```

Where r13, g13, b13, are the RGB values of the central pixel, and y is the class of the central pixel.

The pixels in the window are ordered in the feature vector in row-major order.

## Dataset
[www.cs.toronto.edu/~vmnih/data/](https://www.cs.toronto.edu/~vmnih/data/)

## Limitations
### Dataset size
As mentioned earlier, a per-pixel-classification technique is used, which means that a single pixel generates one feature vector, so an 1500x1500 image will generate 2250000 vectors, which is too large to be handled by a personal computer, that's why the 'convertToFeatureFiles.py' script generates only 200000 vectors per file.

### Features selection
The features considered in this model are the RGB values of the pixels surrounding each pixel, which are not enough because road pixels and non-road pixels made of the same material looks the same, for example road pixels and buildings or parking lots. A possible solution is to add a convolutional neural network as another layer to the model before the used neural network, the added CNN can segment the building based on other features and exclude them before further processing.

## Usage
- Install python and [Tensorflow](https://www.tensorflow.org/) as described [here](https://www.tensorflow.org/install/).
- Install [pillow](https://python-pillow.org/) as described [here](http://pillow.readthedocs.io/en/3.0.x/installation.html).
- Prepare the dataset in the directories contained in 'airs-dataset' directory. Each input image must have a corresponding binary (black and white) output image of the same exact dimensions in the corresponding output directory.
- Run 'convertToFeatureFiles.py'. It should generate three csv files, train.csv, test.csv, and valid.csv.
- Run 'train.py'. It should build the NN, and train it using the generated files in the previous step (this may take several minutes, hours, or days depending on the size of the files, the size of the network, and the number of training iterations).
- Prepare the input image in 'image-input' directory.
- Run 'classify.py' giving it two cmd arguments, the name if the input image file from the previous step, and the desired name of the output image file. It should generate the corresponding binary mask in 'image-output' directory.

## Samples
#### Sample input
![sample input](/image-input/10228690_15.jpg)
#### Expected output
![expected output](/image-output/10228690_15-01.jpg)
#### Output
![output](/image-output/10228690_15-02.jpg)

## Tools
- Python version 3.5.3
- [Tensorflow](https://www.tensorflow.org/) version 1.1.0
- [pillow](https://python-pillow.org/) version 4.1.0

### Notes
- The airs-dataset directory contains a set of images to show the correct directory structure expected by the scripts.
- The images included in this repository are scaled down to reduce their size and should not be used to try the code, use the original dataset images.
