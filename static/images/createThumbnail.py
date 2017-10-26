from PIL import Image
import os

files = os.listdir('./')

for file in files:
	if file.find('.jpg') > 0:
		img = Image.open(file)
		img.thumbnail(128, 128)
		img.save('./thumbnail/' + file)

