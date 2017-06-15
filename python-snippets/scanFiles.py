from os import listdir
from os.path import isfile

path = 'airs-dataset/train-input'
arr = listdir(path)
for idx in range(len(arr)):
	print(path + '/' + arr[idx])

print(len(arr))