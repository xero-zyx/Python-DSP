import scipy.io.wavfile as wavfile
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np

def butterLowPass(samplingFreq, cutoff, order):
    nyquist = 0.5 * samplingFreq
    normCutoff = cutoff / nyquist  # Normalize the cutoff frequency
    if normCutoff <= 0 or normCutoff >= 1:
        raise ValueError("Normalized cutoff frequency must be between 0 and 1")
    b, a = signal.butter(order, normCutoff, btype='low', analog=False)
    return b, a

def butterLowPassFilter(filePath, cutoff, order):
    # Load audio data
    origSamplingRate, audioData = wavfile.read(filePath)

    # If audio data is stereo, convert to mono by averaging the channels
    if len(audioData.shape) == 2:
        audioData = audioData.mean(axis=1)

    # Ensure that the cutoff frequency is less than half the sampling rate (Nyquist frequency)
    if cutoff >= origSamplingRate / 2:
        raise ValueError("Cutoff frequency must be less than half the sampling rate (Nyquist frequency)")

    # Create low-pass IIR filter for the current sampling rate
    b, a = butterLowPass(origSamplingRate, cutoff, order)

    # Apply low-pass IIR filter to the original audio
    filteredAudioData = signal.filtfilt(b, a, audioData)

    # Save the filtered audio
    filteredAudioFile = filePath.replace('.wav', '_lowpass_audio.wav')
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
