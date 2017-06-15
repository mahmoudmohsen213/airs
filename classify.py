from datetime import datetime
from PIL import Image
import sys
import numpy as np
import tensorflow as tf

if(len(sys.argv) != 3):
	raise Exception('invalid command line arguments')

print(str(datetime.now()) + ': initializing input data...')

rectSize = 5;

inputImagePath = 'image-input'
inputImageFile = sys.argv[1]
inputImage = Image.open(inputImagePath + '/' + inputImageFile)
inputImageXSize, inputImageYSize = inputImage.size

outputImagePath = 'image-output'
outputImageFile = sys.argv[2]
outputImage = inputImage.crop((rectSize//2, rectSize//2, inputImageXSize - (rectSize//2), inputImageYSize - (rectSize//2)))
outputImageXSize, outputImageYSize = outputImage.size

print(str(datetime.now()) + ': initializing model...')
featureColumns = [tf.contrib.layers.real_valued_column("", dimension=75)]
# hiddenUnits = [100, 100, 100, 50]
# hiddenUnits = [100, 150, 200, 150, 100, 50]
hiddenUnits = [100, 150, 100, 50]
classes = 2
classifier = tf.contrib.learn.DNNClassifier(feature_columns = featureColumns,
												hidden_units = hiddenUnits,
												n_classes = classes,
												model_dir = 'model')

def extractFeatures():
    features = np.zeros((((inputImageXSize - ((rectSize//2)*2)) * (inputImageYSize - ((rectSize//2)*2))), rectSize*rectSize*3), dtype=np.int)
    rowIndex = 0
    
    for x in range(rectSize//2, inputImageXSize - (rectSize//2)):
        for y in range(rectSize//2, inputImageYSize - (rectSize//2)):            
            rect = (x - (rectSize//2), y - (rectSize//2), x + (rectSize//2) + 1, y + (rectSize//2) + 1)
            subImage = inputImage.crop(rect).load()
            colIndex = 0
            for i in range(rectSize):
                for j in range(rectSize):
                    features[rowIndex, colIndex] = subImage[i, j][0]
                    colIndex += 1
                    features[rowIndex, colIndex] = subImage[i, j][1]
                    colIndex += 1
                    features[rowIndex, colIndex] = subImage[i, j][2]
                    colIndex += 1
            
            rowIndex += 1
    
    return features
    
def constructOutputImage(predictions):
    outputImagePixels = outputImage.load()
    rowIndex = 0
    for x in range(outputImageXSize):
        for y in range(outputImageYSize):
            outputImagePixels[x, y] = ((255, 255, 255) if predictions[rowIndex] else (0, 0, 0))
            rowIndex += 1
        
print(str(datetime.now()) + ': processing image', inputImageFile)
predictions = list(classifier.predict(input_fn=extractFeatures))

print(str(datetime.now()) + ': constructing output image...')
constructOutputImage(predictions)

print(str(datetime.now()) + ': saving output image...')
outputImage.save(outputImagePath + '/' + outputImageFile, 'JPEG')

print(str(datetime.now()) + ': done')