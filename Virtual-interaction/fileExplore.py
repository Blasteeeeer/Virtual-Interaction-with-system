from tkinter import *
from tkinter import filedialog
import glob
import sys
import os
import comtypes.client
from pyfiglet import Figlet
from ppt2pdf.utils import generateOutputFilename
# import pydirectinput as py
# import cv2

import hand_detector_module as htm

def browseFiles():    #(detector, fingers1, fingers2, clocX, clocY, img):
    win = Tk()
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.pptx*"),
                                                     ("all files",
                                                      "*.*")))

    win.destroy()
    return filename


def eraseFile(path):
    files = glob.glob(path + '\\*')
    for f in files:
        os.remove(f)


def ppt2img(inputFilePath, outputFilePath = "C:\\Users\\abdulla khan\\Virtual-interaction\\presentationIMGS"):
    # print("Your Input file is at:")
    # print(inputFilePath)
    if (not outputFilePath):
        outputFilePath = generateOutputFilename(inputFilePath);

    # print("Your Output file will be at:")
    # print(outputFilePath);
    # %% Create powerpoint application object
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    # %% Set visibility to minimize
    powerpoint.Visible = 1
    # %% Open the powerpoint slides
    slides = powerpoint.Presentations.Open(inputFilePath)
    # %% Save as PDF (formatType = 32)
    # %% Save as PNG (formatType = 18)
    slides.SaveAs(outputFilePath, 18)
    # %% Close the slide deck
    slides.Close()
    powerpoint.Quit()
