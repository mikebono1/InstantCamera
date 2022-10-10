import tkinter
from PIL import ImageTk
from tkinter import *
import instantCamera as ic

def scaleImagePreview(im, previewSize):
    #scale image to no bigger than previewSize, keep original scaling
    dim = im.size
    if dim[0] > dim[1]:
        x = previewSize
        y = round((dim[1]/dim[0]) * previewSize)
        return x, y
    elif dim[1] > dim[0]:
        y = previewSize
        x = round((dim[0]/dim[1]) * previewSize)
        return x, y
    else:
        return previewSize, previewSize

def computeImage():
    #compute given image
    global ent
    imageName = ent.get()
    displayInputImage()
    displayOutputImage(ic.main(imageName))

def displayInputImage():
    #display input image in window, but do not compute
    global ent
    imageName = ent.get()
    data, im, newFilePath = ic.openImage(imageName)
    x, y = scaleImagePreview(im, 400)
    im = im.resize((x,y))
    test = ImageTk.PhotoImage(im)
    if 'label1' in locals():
        label1.destroy()
    label1 = Label(image=test)
    label1.imageData = test
    label1.place(x=5,y=90)

def displayOutputImage(im):
    #display computed image in window
    x, y = scaleImagePreview(im, 500)
    im = im.resize((x,y))
    test = ImageTk.PhotoImage(im)
    if 'label2' in locals():
        label2.destroy()
    label2 = Label(image=test)
    label2.imageData = test
    label2.place(x=450,y=25)

#main window
root = tkinter.Tk()
root.title('Instant Camera')
root.geometry('1000x550')

#image name text entry
entLabel = Label(root, text='Image Name').grid(row=1)
ent = Entry(root)
ent.place(x=5,y=5)
ent.focus_set()

#upload image button
uploadImage = Button(root, text='Upload Image', command=displayInputImage)
uploadImage.place(x=5,y=30)

#compute image button
btn = Button(root, text='Compute Image', command=computeImage)
btn.place(x=5,y=60)

#loop window
root.mainloop()