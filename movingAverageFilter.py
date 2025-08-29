import pandas as pd
import matplotlib.pyplot as plt

def loadCSVFile(filePath, dataType):
    # Importing time-series data
    df = pd.read_csv(filePath, index_col='Date', parse_dates=True)

    # Ensure the selected data type column is numeric
    if not pd.api.types.is_numeric_dtype(df[dataType]):
        raise ValueError(f"The selected column '{dataType}' is not numeric.")

    maxNumPoints = len(df)

    # Extract the selected data type column
    selectedData = df[dataType]

    # Calculate 30-day Simple Moving Average (SMA)
    sma30 = selectedData.rolling(30).mean()

    # Remove NULL values
    df.dropna(inplace=True)

    return df, maxNumPoints, selectedData, sma30

def plotData(selectedData, sma30, numPoints):
    plt.figure(figsize=(16, 8))
    start_index = len(selectedData) - numPoints  # Start plotting from the 30th data point onwards
    plt.plot(selectedData.index[start_index:], selectedData[start_index:], label='Data')
    plt.plot(selectedData.index[start_index:], sma30[start_index:], label='SMA30')
    plt.xlabel("Year")
    plt.legend()
    plt.show()
