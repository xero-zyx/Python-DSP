import cv2
import matplotlib.pyplot as plt


def applyEdgeDetectionFilterAndPlot(filePath):
    try:
        origImage = cv2.imread(filePath, cv2.COLOR_BGR2GRAY)

        if origImage is None:
            raise ValueError("Invalid image file")
        
        blurImage = cv2.GaussianBlur(src=origImage, ksize=(3, 5), sigmaX=0.5)

        edgeImage = cv2.Canny(blurImage, 50, 150)
    
        plt.subplot(2, 2, 2)
        plt.imshow(edgeImage, cmap='gray')
        plt.title('Edge Detected Image')
        plt.axis('off')
    except Exception as e:
        print("Error applying edge detection filter:", e)

def applyReverseDetectionFilterAndPlot(filePath):
    try:
        # Load the image using OpenCV
        origImage = cv2.imread(filePath)
        
        if origImage is None:
            raise ValueError("Invalid image file")

        # Convert the image from BGR (OpenCV default) to RGB (matplotlib default)
        coloredImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2RGB)

        # Invert the image
        invertedImage = cv2.bitwise_not(coloredImage)

        # Plotting the original and inverted images
        plt.subplot(2, 2, 1)
        plt.imshow(coloredImage)
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(2, 2, 3)
        plt.imshow(invertedImage)
        plt.title('Inverted Image')
        plt.axis('off')
    except Exception as e:
        print("Error applying reverse detection filter:", e)

def applyImageBlurAndPlot(filePath):
    try:
        origImage = cv2.imread(filePath)  # Load the image
        
        if origImage is None:
            raise ValueError("Invalid image file")

        # Determine the size of the image
        height, width, _ = origImage.shape

        # Calculate the blur kernel size based on image dimensions
        blur_kernel_width = max(int(width / 30), 1)
        blur_kernel_height = max(int(height / 30), 1)

        # Apply Gaussian blur with the calculated kernel size
        blurredImage = cv2.blur(origImage, (blur_kernel_width, blur_kernel_height), 0)

        # Plotting the blurred image
        plt.subplot(2, 2, 4)
        plt.imshow(cv2.cvtColor(blurredImage, cv2.COLOR_BGR2RGB))
        plt.title('Blurred Image')
        plt.axis('off')
    except Exception as e:
        print("Error applying image blur:", e)


def applyFiltersAndShow(filePath):
    plt.figure(figsize=(10, 8))  # Create a figure with a specific size
    applyEdgeDetectionFilterAndPlot(filePath)
    applyReverseDetectionFilterAndPlot(filePath)
    applyImageBlurAndPlot(filePath)  # Add the blurred image
    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()

