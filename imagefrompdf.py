import io
import requests
import random
import time
import fitz
import os
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *
from PIL import Image, ImageTk

def get_image():
    im = requests.get('http://lorempixel.com/' + str(random.randint(300, 400)) + '/' + str(random.randint(70, 120)) + '/')
    return Image.open(io.BytesIO(im.content))
    
class ImageSelect(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        
        #s=ttk.Style()
        #s.theme_use('clam')

        master.resizable(width=False, height=False)
        master.title('Extract image')
        master.iconify = False
        master.deiconify = False
        master.grab_set = True

        image = ImageTk.PhotoImage(get_image())
        self.image = tk.Label(image=image)
        self.image.image = image
        self.image.grid(row=0, column=0, columnspan=4)

        #------------------TIME--------------
        localtime=time.asctime(time.localtime(time.time()))

        #------------------PATH--------------
        pathReal = "D:/.../Extracted_Images"

        #-----------------INFO TOP------------
        self.lblinfo = tk.Label(font=( 'aria' ,30, 'bold' ),text="Extract image(s) from your pdf",fg="steel blue",bd=10,anchor='w')
        self.lblinfo.grid(row=1, column=0, columnspan=5)

        self.lblinfo2 = tk.Label(font=( 'times' ,17, ),text=localtime,fg="black",anchor='w')
        self.lblinfo2.grid(row=2, column=0, columnspan=3)

        #-----------------PDF UPLOAD FILE------------
        self.pdfName = tk.Label(font=( 'times' ,12, ),text="Here will appear the uploaded file's path",fg="black",anchor='w')
        self.pdfName.grid(row=3, column=0, columnspan=2, pady = 50)

        self.buttonUpload = tk.Button(text='Open', command=self.UploadAction)
        self.buttonUpload.grid(row=3, column=2, columnspan=1, pady = 50)

        self.successMsg = tk.Label(font=( 'times' ,12, ),text="No image in this pdf",fg="red",anchor='w')
        self.successMsg.grid(row=3, column=4, columnspan=2, pady = 50)
        self.successMsg.grid_remove()
        
        self.direcName = tk.Label(font=( 'times' ,12, ),text="Images store: " + pathReal,fg="black",anchor='w')
        self.direcName.grid(row=4, column=0, columnspan=5, pady = 5)
    
    def UploadAction(self, event=None):
        filename = filedialog.askopenfilename(initialdir = "/.../KETRIKA/",title = "Select file",filetypes = (("pdf files","*.pdf"),("pdf files","*.pdf*")))
        
        imgdir = r"D:/.../Extracted_Images/"  # where the pics are
        imglist = os.listdir(imgdir)  # list of them
        for f in imglist:
            os.remove(os.path.join(imgdir, f))
        
        #self.pdfName['text'] = filename (an alternative)
        self.pdfName.configure(text = filename)  
        doc = fitz.open(filename)
        nbimage = 0
        for i in range(len(doc)):
            pageImageList = doc.getPageImageList(i)

            if (not len(pageImageList)):
                self.successMsg.configure(text = "No image in this pdf", fg = "green")     
                self.successMsg.grid()  
                return

            for img in pageImageList:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG(imgdir + "p%s-%s.png" % (i, xref))
                    pix = None 
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(imgdir + "p%s-%s.png" % (i, xref))
                    pix1 = None 
                nbimage = nbimage + 1
                
        self.successMsg.configure(font=( 'times' ,12, 'bold'), text = str(nbimage) + " Images extracted", fg = "green")     
        self.successMsg.grid()   

        imglist = os.listdir(imgdir)  # list of them
        #imgcount = len(imglist)  # pic count

        rownumber = 5
        i = 1
        for a, f in enumerate(imglist):
            image = Image.open(imgdir + f)
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            image1 = tk.Label(image=image)
            image1.image = image
            if(i % 5 == 0):
                rownumber = rownumber + 1
                i = 1
            image1.grid(row=rownumber, column=i-1, columnspan=1)
            image = None
            print('Image%s - %s: %s' % (i, rownumber, f))
            i = i + 1             

root = tk.Tk()
app = ImageSelect(master=root)
app.mainloop()
