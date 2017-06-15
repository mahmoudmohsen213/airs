from datetime import datetime
import numpy as np
import tensorflow as tf

print(str(datetime.now()) + ': loading data files')
# Data sets
testDataFileName = 'airs-dataset/test.csv'
# Load datasets.
testData = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename=testDataFileName,
    target_dtype=np.int,
    features_dtype=np.int)

featureColumns = [tf.contrib.layers.real_valued_column("", dimension=75)]
hiddenUnits = [100, 100, 100, 50]
classes = 2
classifier = tf.contrib.learn.DNNClassifier(feature_columns = featureColumns,
                                                hidden_units = hiddenUnits,
                                                n_classes = classes,
                                                model_dir = 'model')
                                                
# Define the test inputs
def getTestData():
    x = tf.constant(testData.data)
    y = tf.constant(testData.target)
    return x, y

print(str(datetime.now()) + ': testing...')
accuracy = classifier.evaluate(input_fn=getTestData, steps=1)['accuracy']
print(str(datetime.now()) + ': done')
print(str(datetime.now()) + ': accuracy:', accuracy)
