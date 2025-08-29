import scipy.io.wavfile as wavfile
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np

cutoff = 4000 
numtaps = 101 

def firFilter(samplingFreq, cutoff, numtaps):
    halfSamplingFreq = samplingFreq / 2
    normCutoff = cutoff / halfSamplingFreq
    filterFIR = signal.firwin(numtaps, normCutoff)
    return filterFIR

def applyAudioFilter(filePath):
    # Load audio data
    origSamplingRate, audioData = wavfile.read(filePath)

    # If audio data is stereo, convert to mono by averaging the channels
    if len(audioData.shape) == 2:
        audioData = audioData.mean(axis=1)

    # Create FIR filter for the current sampling rate
    audioFilter = firFilter(origSamplingRate, cutoff, numtaps)

    # Apply FIR filter
    filteredAudioData = signal.convolve(audioData, audioFilter, mode='same') / np.sum(audioFilter)

    # Save the filtered audio
    filteredAudioFile = filePath.replace('.wav', '_filtered.wav')
    wavfile.write(filteredAudioFile, origSamplingRate, np.int16(filteredAudioData))

    # Time array for plotting
    time = np.arange(len(audioData)) / origSamplingRate

    # Plotting
    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.title('Original Audio Signal')
    plt.plot(time, audioData, label='Original Signal', alpha=0.7)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.title('Low-pass Audio Signal')
    plt.plot(time, filteredAudioData, label='Low-pass Signal', color='green', alpha=0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.plot(time, audioData, label='Original Signal', alpha=0.7)
    plt.plot(time, filteredAudioData, label='Low-pass Signal', color='green', alpha=0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

    return filteredAudioFile