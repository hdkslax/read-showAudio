import tkinter
from tkinter import filedialog
import os
import array
import wave
import matplotlib.pyplot as plt
import numpy as np

root = tkinter.Tk()
root.withdraw() # not show the tk dialog box
wav_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                    title="Please select a file:")
print("文件名为：", wav_path)
wav_file = open(wav_path, 'rb')
wav = wav_file.read()
wav_file = wave.open(wav_path, 'rb')

# wav = wave.open(wav_path,'rb')
params = wav_file.getparams()
wav_length = len(wav)
# buffer = np.array((0 for _ in range(wav_length)))
# for i in range(44, wav_length, 1):
#     buffer[i - 44] = wav[i]
# print(buffer)
# print(len(buffer))

datawav = wav_file.readframes(params[3])
wav_file.close()

wav_data = np.fromstring(datawav,dtype=np.short)
time = np.arange(0,params[3]) * (1.0/params[2])
plt.title("The wav file")
plt.plot(time, wav_data[0], color='green')
plt.plot(time, wav_data[1])
plt.show()


