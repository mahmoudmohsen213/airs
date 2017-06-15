# airs - Aerial Images Road Segmentation

## Problem
Road segmentation is detecting roads in aerial images usually taken by satellites. Specifically, Given an aerial image, it is required to output a binary mask for the input image showing for each pixel if it belongs to a road or not.

## Solution

A per-pixel-classification technique will be used to build the output binary mask, that is, each pixel is independently classified as part of a road or not.

To classify pixel (x, y), the pixels contained in the surrounding window of a predefined side length ‘L’ centered at (x, y) will be used as features, so that the input features vector will contain the (r, g, b) values of all these pixels (including the current target pixel at (x, y)), which makes the features vector size = 3*L*L.

As a classifier, a deep neural network of multiple hidden layers is used. The output layer consists of two neurons representing the two output classes in one-hot vector representation.

## Implementation
The described solution is implemented in python using Tensorflow machine learning library. It consists of four separate python scripts with the following purposes:
- Converting the image data set into three csv text files, train.csv, test.csv and valid.csv used for training, testing and validation respectively.
- Building a classifier, training it using the generated training and testing csv text file, and saving it in a Tensorflow format.
- Loading an already trained classifier, and calculate its accuracy using the generating validation csv text files.
- Classifying an input image.

The first step is converting an image data set into csv data files that can be fed into the classifier for training, testing and validation. The images are divided into training images, testing images and validation images in a predefined directory structure, these directories are scanned by the first script mentioned above.

To obtain good results, the ratio between the samples of the two classes shouldn’t be too large, and naturally the ratio between non-road pixels and road pixels in each image is very large, that’s why dropout must be performed to balance the dataset, but is must be performed in a random fashion to ensure that the classifier is exposed to a diverse set of sample for each class. To perform the dropout for each image, the script loads the image along with its corresponding expected output, then it divides it into two sets of pixel, road pixels and non-road pixels, randomly shuffles both sets, and then for each road pixel, we take two non-road pixels (which ensures the ratio between road samples and non-road samples to be 1:2 in the output csv file), generate their feature vectors as mention earlier, and write them to the output file. This is done for training images, testing images and validation images to generate the three files.

The second step is training the classifier. The second script uses Tensorflow to initialize a deep neural network of four hidden layers of sizes 100, 150, 100, 50 neurons respectively, then loads the training and testing csv file, and use it to train the neural network for a predefined number of iterations, the testing data is used to evaluate the model at the end of each iteration, to prevent over fitting on the training data. After the training finishes, the script saves the model on the file system in a Tensorflow specific format that can be loaded to recalculate its accuracy, or use it in classifying input images.

The third script is used to test the model accuracy, it loads the model and the validation csv file, and calculate its accuracy.

Classification of an input image is done using the fourth script, it takes the names of the input and output image names as command line arguments, it loads the model and the input image from the ‘image-input’ directory, generate the feature vector for each pixel, classify it using the loaded classifier, and generate the output image with zero/one value for each pixel based on the classifier prediction for that pixel, then it saves the generated image in ‘image-output’ directory using the output image name entered in the command line arguments.

## Dataset
[dataset](https://www.cs.toronto.edu/~vmnih/data/).

## Samples



### Notes
- The airs-dataset directory contains a set images to show the correct directory strucure expected by the scripts.
- The images included in this repository are scaled down to reduce their size and should not be used to try the code, use the original dataset images.