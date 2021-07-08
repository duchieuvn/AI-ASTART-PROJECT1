from PIL import Image
import numpy as np

def toMatrix(imagePath):
    img = Image.open(imagePath)
    width, height = img.size
    print()
    rgba = list(img.getdata())

    data = []
    temp = []

    count = 0;
    for row in range(height):
        for col in range(width):
            temp.append(rgba[count][0])
            count += 1

        data.append(temp)
        temp = []

    return data


data = toMatrix('map.bmp')
data = np.array(data)

print('matrix size: ', data.shape)
print("first 10 values: ")
print(data[0][:11])