import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
from scipy.fftpack import fft
import threading
import sys , time


class streamThread(threading.Thread):
    def __init__(self , threadID , name ,mainObject):
        threading.Thread.__init__(self)
        self.threadId = threadID
        self.name = name
        self.mainObject = mainObject
        
    def run(self):
        
        self.createStream()
        
    def createStream(self):
        
        MO = self.mainObject
        stream = MO.p.open(
            format=MO.FORMAT,
            channels=MO.CHANNELS,
            rate=MO.RATE,
            input=True,
            output=True,
            frames_per_buffer=MO.CHUNK,
        )
        
        while not MO.pause:
            
            data = stream.read(MO.CHUNK)
            MO.data_int = struct.unpack(str(2 * MO.CHUNK) + 'B', data)
            MO.data_np = np.array(MO.data_int, dtype='b')[::2] + 128

  
class SpectrumGraph(object):
    def __init__(self , figSizeX , figSizeY , pauseOnClick):
        
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False
        self.figSizeX = figSizeX
        self.figSizeY = figSizeY
        self.pauseOnClick = pauseOnClick
        self.p = pyaudio.PyAudio()
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        data = stream.read(self.CHUNK)
        self.data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)
        self.data_np = np.array(self.data_int, dtype='b')[::2] + 128
        self.p.close(stream)
        
        streamThread(1 , "stream_thread" ,self).start()
        self.init_plots()

    def init_plots(self):

        x = np.arange(0, 2 * self.CHUNK, 2)
        xf = np.linspace(0, self.RATE, self.CHUNK)

        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(self.figSizeX, self.figSizeY))

        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), '-', lw=2)

        self.line_fft, = ax2.semilogx(
            xf, np.random.rand(self.CHUNK), '-', lw=2)

        if self.pauseOnClick:
            self.fig.canvas.mpl_connect('button_press_event' , self.onClick)
        ax1.set_title('WAVEFORM')
        ax1.set_xlabel('samples')
        ax1.set_ylabel('volume')
        ax1.set_ylim(0, 255)
        ax1.set_xlim(0, 2 * self.CHUNK)
        plt.setp(
            ax1, yticks=[0, 128, 255],
            xticks=[0, self.CHUNK, 2 * self.CHUNK],
        )
        plt.setp(ax2, yticks=[0, 1],)

        ax2.set_xlim(20, self.RATE / 2)

        thismanager = plt.get_current_fig_manager()
        thismanager.window.wm_geometry("+700+400")

        plt.show(block=False)

    def start_plot(self):
        
        while not self.pause:
            
            self.line.set_ydata(self.data_np)
            
            yf = fft(self.data_int)
            self.line_fft.set_ydata(
                np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK))

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
    def end_plot(self):
        
        self.p.close(self.stream)
        
    def onClick(self , event):
        
        self.pause = True
