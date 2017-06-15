from PIL import Image

i = Image.open('airs-dataset/train-input/10228705_15.tiff')
# i.show()
xsize, ysize = i.size
pixels = i.load()

flag =  ((pixels[100, 100][0] != 0) and (pixels[100, 100][1] != 0) and (pixels[100, 100][2] != 0))

print(str(pixels[100, 100]))
print(flag)

pixels[100, 100] = (0, 0, 0)
flag =  ((pixels[100, 100][0] == 0) and (pixels[100, 100][1] == 0) and (pixels[100, 100][2] == 0))
print(str(pixels[100, 100]))
print(flag)

for x in range(100):
	for y in range(100):
		pixels[100+x,100+y] = (0, 0, 0)

# i.save('newImage.jpg', 'JPEG')