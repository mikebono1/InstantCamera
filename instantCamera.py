from PIL import Image
import logging
import numpy as np
import os
import time

def openImage(imageName):
    #open the requested image
    imagePath = x = 0
    fileTypes = ['jpeg', 'png']
    savePath = f'instantCamera/images/{imageName}Normalized.png'
    while os.path.isfile(imagePath) is False:
        imagePath = f'instantCamera/images/{imageName}.{fileTypes[x]}'
        x = x + 1
    im = Image.open(imagePath)
    #open image as array of pixel values
    a = np.asarray(im)
    return a, im, savePath

def formatData(a):
    #determine color space of image
    size = a.shape
    if len(size) == 2:
        logging.error("Greyscale images not yet supported")
    elif len(size) == 3:
        #turn rgb image into 3 seperate arrays, one for R, G, and B
        rImage = a[...,0]
        gImage = a[...,1]
        bImage = a[...,2]
        image = np.array([rImage, gImage, bImage])
    else:
        logging.error("Image color format not yet supported")
    return image

def redmean(rgb1, rgb2):
    #define average red color and difference between given RGB values
    avgR = (rgb1[0] + rgb2[0])/2
    dR = rgb1[0] - rgb2[0]
    dG = rgb1[1] - rgb2[1]
    dB = rgb1[2] - rgb2[2]
    #calculate redmean
    dC = pow(((2+(avgR/256))*pow(dR,2)) + (4*pow(dG,2)) + (2+(((255-avgR)/256))*pow(dB,2)),0.5)
    return dC

def calcRedmean(image):
    #compute average redmean over every pixel position in image (except for 1px by 1px border)
    size = image.shape
    logging.info(size)
    z, y, x = size
    lDiff = redmean(image[:, 1:y-1, 1:x-1], image[:, 1:y-1, 0:x-2])
    rDiff = redmean(image[:, 1:y-1, 1:x-1], image[:, 1:y-1, 2:x])
    tDiff = redmean(image[:, 1:y-1, 1:x-1], image[:, 0:y-2, 1:x-1])
    bDiff = redmean(image[:, 1:y-1, 1:x-1], image[:, 2:y, 1:x-1])
    diff = np.minimum(np.minimum(rDiff,lDiff), np.minimum(tDiff,bDiff))
    #average of color differences
    avgDiff = (np.average(lDiff) + np.average(rDiff) + np.average(tDiff) + np.average(bDiff)) / 4
    return diff, avgDiff

def cleanData(data):
    diff, avgDiff = data
    #all color differences less than average are irrelevant
    diff[diff <= avgDiff] = 0
    #give different wieghts to data
    diff = pow(diff, 2)
    #remap data from values between 0 and 255
    minVal = np.min(diff)
    maxVal = np.max(diff)
    cleanArr = (((diff - minVal) / (maxVal - minVal)) * 255)
    return cleanArr

def main(imageName):
    #set up logging module
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s -> %(message)s'
    logging.basicConfig(level=level, format=fmt)

    #given image name, compute important color change positions
    rawData, filePath, savePath = openImage(imageName)
    start = time.perf_counter()
    formData = formatData(rawData)
    data = calcRedmean(formData)
    imageData = cleanData(data)
    im = Image.fromarray(imageData)
    end = time.perf_counter()
    logging.info(round(end - start, 4))
    # im.show()
    return im