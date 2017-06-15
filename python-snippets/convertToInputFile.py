from os import listdir
from PIL import Image
from datetime import datetime

inputImagePath = 'image-input'
inputImageFiles = listdir(inputImagePath)

print('inputImagesFiles:', len(inputImageFiles))

def writeInputFile(inputImagePath, inputImageFiles):
    rectSize = 5;
    
    for i in range(len(inputImageFiles)):
        print(str(datetime.now()) + ': prcessing image', i)
        
        metaDataFile = open(inputImagePath + '/' + inputImageFiles[i] + '.meta', 'w')
        dataFile = open(inputImagePath + '/' + inputImageFiles[i] + '.csv', 'w')
        inputImage = Image.open(inputImagePath + '/' + inputImageFiles[i])
        inputImageXSize, inputImageYSize = inputImage.size
        inputImagePixels = inputImage.load()
        
        metaDataFile.write(str(inputImageXSize) + '\n')
        metaDataFile.write(str(inputImageYSize) + '\n')
        metaDataFile.write(str(rectSize) + '\n')
        
        for x in range(rectSize//2, inputImageXSize - (rectSize//2)):
            for y in range(rectSize//2, inputImageYSize - (rectSize//2)):
                rect = (x - (rectSize//2), y - (rectSize//2), x + (rectSize//2) + 1, y + (rectSize//2) + 1)
                subImage = inputImage.crop(rect).load()
                line = ''
                for i in range(rectSize):
                    for j in range(rectSize):
                        line += str(subImage[i, j][0]) + ','
                        line += str(subImage[i, j][1]) + ','
                        line += str(subImage[i, j][2]) + ','
                
                line = line[:-1]
                dataFile.write(line + '\n')

writeInputFile(inputImagePath, inputImageFiles)
# END