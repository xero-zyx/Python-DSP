import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
import adcFilter
import firAudioFilter
import firImageFilter
import movingAverageFilter
import highPassLowPassFilter
import pandas as pd

def applyHoverStyle(button):
    def onEnter(e):
        button.config(bg="#606060", fg="white")

    def onLeave(e):
        button.config(bg="SystemButtonFace", fg="black")

    button.bind("<Enter>", onEnter)
    button.bind("<Leave>", onLeave)

def adcTab(tab):
    fontLabel = font.Font(font=("Segoe UI", 12))  # Increased font size for labels
    fontBox = font.Font(font=("Segoe UI", 12))  # Increased font size for entries

    # Frequency 1 input
    samplingFreqLabel = tk.Label(tab, text="Sampling Frequency (Hz):", font=fontLabel)
    samplingFreqLabel.grid(row=0, column=0, padx=20, pady=150, sticky="e")
    samplingFreqBox = tk.Entry(tab, font=fontBox)
    samplingFreqBox.grid(row=0, column=1, padx=20, pady=150, sticky="w")

    # Button to apply filter
    def plotADCButton():
        try:
            samplingFrequency = int(samplingFreqBox.get())
            if samplingFrequency > 1000:
                messagebox.showwarning("Frequency Warning", "The sampling frequency is greater than 1000 Hz.")
                return
            adcFilter.sampleSignal(samplingFrequency)
        except ValueError:
            if not samplingFreqBox.get():
                messagebox.showwarning("Input Required", "Please enter a sampling frequency.")
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the sampling frequency.")

    buttonPlot = tk.Button(tab, text="     Plot     ", command=plotADCButton, font=fontLabel)
    buttonPlot.grid(row=1, column=0, padx=20, pady=30)
    applyHoverStyle(buttonPlot)

    # Clear all inputs
    def clearButton():
        samplingFreqBox.delete(0, tk.END)

    buttonClear = tk.Button(tab, text="     Clear     ", command=clearButton, font=fontLabel)
    buttonClear.grid(row=1, column=1, padx=20, pady=30)
    applyHoverStyle(buttonClear)

    for i in range(2):
            tab.grid_rowconfigure(i, minsize=50)  # Ensure space for buttons
            tab.grid_columnconfigure(i, weight=1)  # Columns take all extra space

def firTab(tab):
    fontLabel = font.Font(font=("Segoe UI", 12))  # Increased font size for labels

    # Variable to store the selected filter type
    filterType = tk.StringVar(value="")  # Initially set to empty string

    # Radio buttons to select filter type
    style = ttk.Style()
    style.configure("TRadiobutton", font=("Segoe UI", 12), background="#F0F0F0")

    audioFilterRadio = ttk.Radiobutton(tab, text="Audio Filter", variable=filterType, value="audio", style="TRadiobutton")
    audioFilterRadio.grid(row=0, column=0, padx=20, pady=50)
    audioFilterLabel = tk.Label(tab, text="WAV files, *.wav", font=fontLabel)
    audioFilterLabel.grid(row=1, column=0, padx=20)
    imageFilterRadio = ttk.Radiobutton(tab, text="Image Filter", variable=filterType, value="image", style="TRadiobutton")
    imageFilterRadio.grid(row=0, column=1, padx=20, pady=50)
    imageFilterLabel = tk.Label(tab, text="Image files, *.png;*.jpg;*.jpeg", font=fontLabel)
    imageFilterLabel.grid(row=1, column=1, padx=20)

    # File path variable
    filePath = tk.StringVar()

    # Label to display the selected file path
    filePathLabel = tk.Label(tab, textvariable=filePath, font=fontLabel)
    filePathLabel.grid(row=2, column=0, columnspan=2, pady=50)

    def selectFile():
        fileType = [("WAV files", "*.wav"), ("Image files", "*.png;*.jpg;*.jpeg")] if filterType.get() == "audio" else [
            ("Image files", "*.png;*.jpg;*.jpeg")]
        path = filedialog.askopenfilename(filetypes=fileType)
        if path:
            filePath.set(path)
    
    # Button to select file
    selectFileButton = tk.Button(tab, text="     Select File     ", command=selectFile, font=fontLabel)
    selectFileButton.grid(row=3, column=0, padx=20, pady=20)
    applyHoverStyle(selectFileButton)

    # Clear selected file
    def clearFileSelection():
        filePath.set("")
        filterType.set("")

    # Button to clear file selection
    clearButton = tk.Button(tab, text="     Clear     ", command=clearFileSelection, font=fontLabel)
    clearButton.grid(row=3, column=1, padx=20, pady=20)
    applyHoverStyle(clearButton)

    def applyFilter():
        try:
            if filePath.get():
                if filterType.get() == "audio":
                    firAudioFilter.applyAudioFilter(filePath.get())
                elif filterType.get() == "image":
                    firImageFilter.applyFiltersAndShow(filePath.get())
            else:
                messagebox.showwarning("No file selected", "Please select a file first.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Button to apply filter
    applyFilterButton = tk.Button(tab, text="     Apply Filter     ", command=applyFilter, font=fontLabel)
    applyFilterButton.grid(row=5, column=0, columnspan=2, padx=20, pady=50)
    applyHoverStyle(applyFilterButton)
    
    # Configuring rows and columns to keep the UI elements centered
    for i in range(4):
        tab.grid_rowconfigure(i, weight=1 if i in [0, 1] else 2)  # For the first two rows, weight is 1, for the other rows, weight is 2

    for i in range(2):
        tab.grid_columnconfigure(i, weight=1)  # Data type radio buttons

def movingAverageTab(tab):
    fontLabel = font.Font(font=("Segoe UI", 12))  # Increased font size for labels

    dataPointsLabel = tk.Label(tab, text="Select CSV File and Data Type to Plot", font=fontLabel)
    dataPointsLabel.grid(row=0, column=0, columnspan=7, pady=25, sticky="ew")

    # File path variable
    filePath = tk.StringVar()

    # Label to display the selected file path
    filePathLabel = tk.Label(tab, textvariable=filePath, font=fontLabel)
    filePathLabel.grid(row=2, column=0, columnspan=7, sticky="ew")

    dataType = tk.StringVar()

    # Frame to hold radio buttons
    radioFrame = tk.Frame(tab)
    radioFrame.grid(row=1, column=0, columnspan=7, pady=10, sticky="ew")

    def createRadioButtons(columns):
        for widget in radioFrame.winfo_children():
            widget.destroy()
        num_columns = len(columns)
        for i, column in enumerate(columns):
            if column != 'Date':  # Skip Date column
                csvRadioButton = ttk.Radiobutton(radioFrame, text=column, value=column, variable=dataType, style="TRadiobutton")
                csvRadioButton.grid(row=0, column=i, padx=5, sticky="ew")
        for i in range(num_columns):
            radioFrame.grid_columnconfigure(i, weight=1)

    def selectCSVFile():
        csvFile = [("CSV files", "*.csv")]
        textPath = filedialog.askopenfilename(filetypes=csvFile)
        if textPath:
            filePath.set(textPath)
            try:
                # Read the CSV file to get column headers
                df = pd.read_csv(textPath)
                columns = df.columns.tolist()
                createRadioButtons(columns)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file: {e}")

    # Button to select file
    selectFileButton = tk.Button(tab, text="Select CSV File", command=selectCSVFile, font=fontLabel)
    selectFileButton.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

    def plotGraph():
        try:
            textPath = filePath.get()
            if textPath:
                dataTypes = dataType.get()
                reliance, maxNumPoints, selectedData, sma30 = movingAverageFilter.loadCSVFile(textPath, dataTypes)
                movingAverageFilter.plotData(selectedData, sma30, maxNumPoints)
            else:
                messagebox.showwarning("No File Selected", "Please select a CSV file first.")
        except ValueError as e:
            messagebox.showerror("Error", f"{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Button to plot graph
    plotGraphButton = tk.Button(tab, text="Plot", command=plotGraph, font=fontLabel)
    plotGraphButton.grid(row=3, column=3, padx=20, pady=20, sticky="ew")

    # Clear all inputs
    def clearInputs():
        filePath.set("")
        dataType.set("")
        for widget in radioFrame.winfo_children():
            widget.destroy()

    clearButton = tk.Button(tab, text="Clear", command=clearInputs, font=fontLabel)
    clearButton.grid(row=3, column=5, padx=20, pady=20, sticky="ew")

    # Configuring rows and columns to keep the UI elements centered
    for i in range(4):
        tab.grid_rowconfigure(i, weight=1)

    # Adding empty columns on both sides and setting weights
    for i in range(7):
        tab.grid_columnconfigure(i, weight=1)

def highLowTab(tab):
    fontLabel = font.Font(font=("Segoe UI", 12))  # Correct font configuration
    fontBox = font.Font(font=("Segoe UI", 12))  # Increased font size for entries

    # Cutoff Frequency input
    cutoffFreqLabel = tk.Label(tab, text="Cutoff Frequency:", font=fontLabel)
    cutoffFreqLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=50)
    cutoffFreqBox = tk.Entry(tab, font=fontBox)
    cutoffFreqBox.grid(row=0, column=1, columnspan=2, padx=20, pady=50)

    # Order input
    orderLabel = tk.Label(tab, text="Order (1-10):", font=fontLabel)
    orderLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=50)
    orderBox = tk.Entry(tab, font=fontBox)
    orderBox.grid(row=1, column=1, columnspan=2, padx=20, pady=50)

    # File path variable
    filePath = tk.StringVar()

    # Label to display the selected file path
    filePathLabel = tk.Label(tab, textvariable=filePath, font=fontLabel)
    filePathLabel.grid(row=2, column=0, columnspan=3, pady=50)

    def selectAudioFile():
        audioFile = [("WAV files", "*.wav")]
        path = filedialog.askopenfilename(filetypes=audioFile)
        if path:
            filePath.set(path)

    # Button to select file
    selectFileButton = tk.Button(tab, text="     Select Audio File     ", command=selectAudioFile, font=fontLabel)
    selectFileButton.grid(row=3, column=0, padx=20, pady=30)
    applyHoverStyle(selectFileButton)

    def applyLowPass():
        try:
            if filePath.get():
                cutoffData = cutoffFreqBox.get()
                orderData = orderBox.get()
                if not cutoffData or not orderData:
                    messagebox.showwarning("Invalid input", "Please enter both cutoff frequency and order.")
                    return

                cutoff = int(cutoffData)
                order = int(orderData)
                if order > 10:
                    messagebox.showerror("Invalid input", "Order must be 10 or lower.")
                    return

                highPassLowPassFilter.butterLowPassFilter(filePath.get(), cutoff, order)
            else:
                messagebox.showwarning("No file selected", "Please select a file first.")
        except ValueError as ve:
            messagebox.showerror("Invalid input", f"Invalid input: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Button to apply filter
    applyFilterButton = tk.Button(tab, text="     Apply Filter     ", command=applyLowPass, font=fontLabel)
    applyFilterButton.grid(row=3, column=1, padx=20, pady=30)
    applyHoverStyle(applyFilterButton)

    # Clear all inputs
    def clearNumpoints():
        cutoffFreqBox.delete(0, tk.END)
        orderBox.delete(0, tk.END)
        filePath.set("")

    clearButton = tk.Button(tab, text="     Clear     ", command=clearNumpoints, font=fontLabel)
    clearButton.grid(row=3, column=2, padx=20, pady=20)
    applyHoverStyle(clearButton)

    # Configuring rows and columns to keep the UI elements fixed
    for i in range(4):
        tab.grid_rowconfigure(i, minsize=50)  # Ensures space for buttons
    
    for i in range(3):
        tab.grid_columnconfigure(i, weight=1)  # Columns take all extra space

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__() 

        self.title("Python GUI DSP Application")
        self.geometry("800x600")
        self.resizable(False, False)

        # Center the window
        windowWidth = 800
        windowHeight = 600
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        positionTop = int(screenHeight / 2 - windowHeight / 2)
        positionRight = int(screenWidth / 2 - windowWidth / 2)
        self.geometry(f'{windowWidth}x{windowHeight}+{positionRight}+{positionTop}')

        # Adjusting the style to match Windows 11 aesthetics
        style = ttk.Style(self)
        style.configure("TNotebook.Tab", padding=[10, 5], font=("Segoe UI", 10), background="#F0F0F0")  # Tab appearance

        ribbonTab = ttk.Notebook(self)

        tabADC = ttk.Frame(ribbonTab)
        tabFIR = ttk.Frame(ribbonTab)
        tabMovingAverage = ttk.Frame(ribbonTab)
        tabHighLow = ttk.Frame(ribbonTab)

        ribbonTab.add(tabADC, text="       ADC Conversion       ")
        ribbonTab.add(tabFIR, text="       FIR Filter       ")
        ribbonTab.add(tabMovingAverage, text="       Moving Average Filter       ")
        ribbonTab.add(tabHighLow, text="       High-pass to Low-pass Filter Conversion       ")

        ribbonTab.pack(fill=tk.BOTH, expand=True)

        adcTab(tabADC)
        firTab(tabFIR)
        movingAverageTab(tabMovingAverage)
        highLowTab(tabHighLow)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
