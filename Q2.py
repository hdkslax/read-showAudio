import tkinter
from tkinter import *
from tkinter import filedialog
import os
import array



# reads a .wav files
def read_wav():
    root = tkinter.Tk()
    root.withdraw() # not show the tk dialog box
    wav_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                    title="Please select a wav file:")
    if wav_path == '':
        exit()
    return wav_path

def wav_to_binary(file_path):
    global nframes
    wav_file = open(file_path, 'rb')
    wav = wav_file.read()
    wav_length = len(wav)

    header = array.array('i', (0 for _ in range(44)))
    data = array.array('i', (0 for _ in range(wav_length-44)))

    # store header info in array header
    for k in range(44):
        header[k] = wav[k]
    # store frames in array buffer
    for i in range(44, len(wav), 1):
        data[i-44] = wav[i]
    # print("data = ", data)

    if header[34] == 16:
        nframes = (int)((wav_length - 44) / 2)
    elif header[34] == 8:
        nframes = wav_length-44
    elif header[34] == 24:
        nframes = (int)((wav_length-44) / 3)
    else:
        print("Sorry, we don't support this file")
        exit()

    # print("nframes = ", nframes)
    frames = array.array('i', (0 for _ in range(nframes)))
    # store samples in frames array
    if header[34] == 16:
        for j in range(len(frames)):
            frames[j] = 16*16*data[j*2+1] + data[j*2]
            if frames[j] > 32767:
                frames[j] = frames[j] - 65536
    elif header[34] == 8:
        for j in range(len(frames)):
            frames[j] = data[j]
            if frames[j] > 128:
                frames[j] = frames[j] - 256
    elif header[34] == 24:
        for j in range(len(frames)):
            frames[j] = 16*16*16*16*data[j*3+2]+16*16*data[j*3+1] + data[j*3]
            if frames[j] > 8388608:
                frames[j] = frames[j] - 16777216
    print("frames = ", frames)

    print(len(data))
    wav_file.close()

    return header, frames

# change the wav to fade-in and fade_out

def fade_in_out(frames):
    middle = int(len(frames) / 2)
    faded_frames = array.array('f', (0 for _ in range(len(frames))))
    for i in range(middle):
        faded_frames[i] = frames[i]*i/middle

    for i in range(middle, len(frames)):
        faded_frames[i] = frames[i]*(len(frames)-i)/middle

    return faded_frames

# return the maximum absolute value in the frames
def maxabs(frames):
    m = abs(frames[0])
    for i in range(1, len(frames)):
        n = abs(frames[i])
        if m < n:
            m = n
    return m

# return the total number of the samples
def nsamples(frames):
    return len(frames)


def plot_frames(header, frames, faded_frames, wav_path):
    tk = Tk()
    tk.geometry('1000x700')
    title = wav_path.split('/')
    title = title[-1]
    tk.title(title)
    tk.config(bg='lightgray')


    # a canvas to show the wave graph
    canvas = Canvas(tk, bg='black', width=900, height=500)
    canvas.place(x=50, y=20)

    # a frame to contain buttons
    btn_frame = Frame(tk)
    btn_frame.config(bg="lightgray", height=100, width=200)
    btn_frame.place(x=50, y=550)

    def open_another_file():
        tk.destroy()
        main()

    # an open button to open another wav file
    open_btn = Button(btn_frame,
                      borderwidth=3,
                      background="grey",
                      overrelief='sunken',
                      text="open another file",
                      command=open_another_file)
    open_btn.place(x=0, y=0)

    # a close button to close the graph GUI
    close_btn = Button(btn_frame,
                       borderwidth=3,
                       background="grey",
                       text='close',
                       overrelief='sunken',
                       command=tk.destroy)
    close_btn.place(x=0, y=40, anchor='nw')

    # a exit button to exit the program
    exit_btn = Button(btn_frame,
                      borderwidth=3,
                      background='grey',
                      text='exit',
                      overrelief='sunken',
                      command=exit)
    exit_btn.place(x=50, y=40, anchor='nw')

    info_frame = Frame(tk)
    info_frame.config(height=100, width=600)
    info_frame.place(x=300, y=550)

    info_canvas = Canvas(info_frame, bg="gray", width=600, height=100)
    info_canvas.pack()

    info_canvas.create_text(200, 20, fill="black", text="Information Board")
    max_abs = "The maximum value among the the samples is: " + str(maxabs(frames))
    num_samples = "The total number of the samples is: " + str(nsamples(frames))
    info_canvas.create_text(200, 50, fill="black", text=max_abs)
    info_canvas.create_text(200, 80, fill="black", text=num_samples)

    print("The total number of the samples is: ", nsamples(frames))

    # the coordinate origin
    x0 = 50
    y0 = 250


    # draw the axis
    nframes = len(frames)
    frame_rate = 16*16*16*16*16*16*header[27] + 16*16*16*16*header[26] + 16*16*header[25] + header[24]
    time = nframes/frame_rate

    canvas.create_line(50,480, 790,480, fill="white", arrow=LAST) # x
    canvas.create_line(50,480, 50,10, fill="white", arrow=LAST) # y

    # units on x-axis
    x_range = int(time * 10 + 2)
    for i in range(1,x_range):
        x = i*700/x_range
        canvas.create_line(x+x0, 480, x+x0, 475, fill="white")
        canvas.create_text(x+x0, 490, fill="white", text=str(round(0.1*i,1)))
    canvas.create_text(780, 490, fill="white", text="time")

    start = 0
    end = 0
    step = 0
    # units on y-axis
    if header[34] == 16:
        start = -30000
        end = 40000
        step = 10000
    elif header[34] == 8:
        start = -120
        end = 120
        step = 40
    elif header[34] == 24:
        start = -8000000
        end = 8000000
        step = 1000000
    elif header[34] == 32:
        start = -2000000000
        end = 2000000000
        step = 500000000

    for i in range(start, end, step):
        y = (i/step) * 60
        canvas.create_line(x0, y+y0, x0+5, y+y0, fill="white")
        canvas.create_text(x0-25, y+y0, fill="white", text=str(-i))


    # calculate x
    sample_time = 1/frame_rate
    print("sample time = ", sample_time)
    def x(t):
        x = x0 + 10 * 700/x_range * (t * sample_time)
        return x

    def y(t):
        y = (y0-faded_frames[t]/step*60)
        return y

    for t in range(0, nframes-1, 1):
        canvas.create_line(x(t), y(t), x(t+1), y(t+1), fill="green")
    tk.mainloop()



def main():
    wav_path = read_wav()
    header, frames = wav_to_binary(wav_path)
    print("header = ", header)
    faded_frames = fade_in_out(frames)
    print("The maximum value among the the samples is: ", maxabs(frames))
    print("The total number of the samples is: ", nsamples(frames))
    plot_frames(header,frames, faded_frames, wav_path)

if __name__ == '__main__':
    main()