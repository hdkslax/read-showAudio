import wave as we
import numpy as np
import os
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt

def wavread(path):
    wavfile = we.open(path, 'rb')
    params = wavfile.getparams()
    framesra,frameswav = params[2], params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.frombuffer(datawav,dtype=np.short)
    time = np.arange(0, frameswav) * (1.0/framesra)
    return datause, time

def main():
    root = tkinter.Tk()
    root.withdraw()  # not show the tk dialog box
    wav_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Please select a file:")
    wavdata, wavtime = wavread(wav_path)
    plt.title("the graph of the wav file")
    plt.plot(wavtime, wavdata, color='green')
    plt.show()

if __name__ == '__main__':
    main()