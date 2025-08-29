import numpy as np
import matplotlib.pyplot as plt

def sampleSignal(samplingFrequency):
    t = np.linspace(0, 1, 1000)
    analogSignal = np.sin(2 * np.pi * 5 * t)
    samplingPoints = np.arange(0, len(t), len(t) // int(samplingFrequency))
    sampledSignal = analogSignal[samplingPoints]
    samplingTimes = t[samplingPoints]

    plt.figure(figsize=(10, 8))

    # Plot Analog Signal
    plt.subplot(3, 1, 1)
    plt.plot(t, analogSignal, label='Analog Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Analog Signal')
    plt.legend()
    plt.grid(True)

    # Plot Sampled Signal
    plt.subplot(3, 1, 2)
    plt.plot(t, analogSignal, label='Analog Signal')
    plt.plot(samplingTimes, sampledSignal, 'ro', label='Sampled Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Sampled Signal')
    plt.legend()
    plt.grid(True)

    # Plot Digital Signal
    plt.subplot(3, 1, 3)
    plt.plot(t, analogSignal, label='Analog Signal')
    plt.vlines(samplingTimes, 0, sampledSignal, colors='green', linestyles='-', label='Digital Signal')
    for i in range(len(samplingTimes) - 1):
        plt.plot([samplingTimes[i], samplingTimes[i + 1]], [sampledSignal[i], sampledSignal[i]], color='green', linestyle='-')
        plt.plot([samplingTimes[i + 1], samplingTimes[i + 1]], [sampledSignal[i], sampledSignal[i + 1]], color='green', linestyle='-')
        plt.plot([samplingTimes[i], samplingTimes[i + 1]], [0, 0], color='blue', linestyle='--')
        plt.plot([samplingTimes[i + 1], samplingTimes[i + 1]], [0, sampledSignal[i + 1]], color='blue', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Digital Signal')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
