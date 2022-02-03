#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np #additional line 
from scipy.io import wavfile
from scipy.fftpack import fft,fftfreq
from sklearn import preprocessing
import threading
import pyaudio
import wave
import time

plot_flag = 1
timer_flag = 0
fftabs2=0
fftabs=0
def generate_wav():    
    CHUNK = 1024*2
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100 #44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "outputHz.wav"    
    p = pyaudio.PyAudio()    
    stream = p.open(rate=RATE,
                    channels=CHANNELS,     
                    format=FORMAT,                 
                    input=True,
                    input_device_index= 2   ,
                    frames_per_buffer=CHUNK)    
    print("* recording")        
    frames = []    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)    
    print("* done recording")    
    stream.stop_stream()
    stream.close()
    p.terminate()    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    global plot_flag
    plot_flag= 1                    

#########################################
def plot_fft():
    global timer_flag
    global fftabs2
    global fftabs
    samplerate, data = wavfile.read("outputHz.wav")
    samples = data.shape[0]
    datafft = fft(data)
    fftabs = abs(datafft)
    freqs = fftfreq(samples,1/samplerate)
    fftabs = preprocessing.normalize([fftabs])
    fftabs = np.transpose(fftabs)
        
    #%matplotlib tk                
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))        
    ax1.set_xlim([10, samplerate/2] )        
    ax1.plot(freqs[:int(freqs.size/2)],fftabs[:int(freqs.size/2)])
    ax1.set_xscale('log')
    ax1.grid( True )
    ax1.set_xlabel('Frequency (Hz)')
    
    ##############################################    
    samplerate2, data2 = wavfile.read("reference.wav")
    samples2 = data2.shape[0]
    datafft2 = fft(data2)
    fftabs2 = abs(datafft2)
    freqs2 = fftfreq(samples2,1/samplerate2)    
    fftabs2 = preprocessing.normalize([fftabs2])
    fftabs2 = np.transpose(fftabs2)        
    
    ax2.set_xlim([10, samplerate/2] )    
    ax2.plot(freqs2[:int(freqs2.size/2)],fftabs2[:int(freqs2.size/2)])
    ax2.set_xscale('log')
    ax2.grid( True )
    ax2.set_xlabel('Frequency (Hz)')        
    
    timer_flag = 1
    
    slice_len = 10
    thresh = 0.00000001
    overlap_x = []        
    for i in range(int(freqs.size/2)-slice_len):      
        #print(abs(fftabs[i]-fftabs2[i]) )
        if abs(fftabs[i]-fftabs2[i]) < thresh:            
            overlap_x.append(3)
    
    
    match_percent = len(overlap_x)*100/(freqs2.size/2)    
    match_percent = (int(match_percent*100))/100    
    
    ax1.set_title('percentage match: '+str(match_percent) +'%' )
    plt.show()
    
    
    #############################################
while True:    
    plot_fft()   
    if timer_flag == 1:
        time.sleep(5) #set timer =5s
        timer_flag = 0
        generate_wav()
    
        


