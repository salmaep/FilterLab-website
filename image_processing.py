import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import Counter
from pylab import savefig
import cv2
import matplotlib
import random
import mahotas as mh
matplotlib.use('Agg')

def grayscale():
    if not is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr/3).astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True


def zoomin():
    if is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        
        if len(img_arr.shape) == 3:
            # Convert grayscale to 2D array
            img_arr = img_arr[:, :, 0]

        new_size = (img_arr.shape[0] * 2, img_arr.shape[1] * 2)
        new_arr = np.full(new_size, 255, dtype=np.uint8)

        for i in range(len(img_arr)):
            for j in range(len(img_arr[i])):
                new_arr[2*i, 2*j] = img_arr[i, j]
                new_arr[2*i, 2*j+1] = img_arr[i, j]
                new_arr[2*i+1, 2*j] = img_arr[i, j]
                new_arr[2*i+1, 2*j+1] = img_arr[i, j]

        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")
    else:
        img = Image.open("static/img/img_now.jpg")
        img = img.convert("RGB")
        img_arr = np.asarray(img)
        new_size = ((img_arr.shape[0] * 2),
                    (img_arr.shape[1] * 2), img_arr.shape[2])
        new_arr = np.full(new_size, 255)
        new_arr.setflags(write=1)

        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]

        new_r = []
        new_g = []
        new_b = []

        for row in range(len(r)):
            temp_r = []
            temp_g = []
            temp_b = []
            for i in r[row]:
                temp_r.extend([i, i])
            for j in g[row]:
                temp_g.extend([j, j])
            for k in b[row]:
                temp_b.extend([k, k])
            for _ in (0, 1):
                new_r.append(temp_r)
                new_g.append(temp_g)
                new_b.append(temp_b)

        for i in range(len(new_arr)):
            for j in range(len(new_arr[i])):
                new_arr[i, j, 0] = new_r[i][j]
                new_arr[i, j, 1] = new_g[i][j]
                new_arr[i, j, 2] = new_b[i][j]

        new_arr = new_arr.astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def zoomout():
    if is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        
        if len(img_arr.shape) == 3:
            # Convert grayscale to 2D array
            img_arr = img_arr[:, :, 0]

        x, y = img_arr.shape
        new_arr = np.zeros((int(x / 2), int(y / 2)), dtype=np.uint8)

        for i in range(0, int(x/2)):
            for j in range(0, int(y/2)):
                new_arr[i, j] = np.mean(img_arr[2*i:2*i+2, 2*j:2*j+2])

        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")
    else:
        img = Image.open("static/img/img_now.jpg")
        img = img.convert("RGB")
        x, y = img.size
        new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
        r = [0, 0, 0, 0]
        g = [0, 0, 0, 0]
        b = [0, 0, 0, 0]

        for i in range(0, int(x/2)):
            for j in range(0, int(y/2)):
                r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
                r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
                r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
                r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
                new_arr.putpixel((int(i), int(j)), (int((r[0] + r[1] + r[2] + r[3]) / 4), int(
                    (g[0] + g[1] + g[2] + g[3]) / 4), int((b[0] + b[1] + b[2] + b[3]) / 4)))
        new_arr = np.uint8(new_arr)
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def move_left():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
        g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
        b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
        new_arr = np.dstack((r,g,b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 0), (50,0)), 'constant')[:, :-50]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
        g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
        b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
        new_arr = np.dstack((r,g,b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:,:]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
        g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
        b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
        new_arr = np.dstack((r,g,b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50,:]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        new_arr = np.dstack((r,g,b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def convolution(img, kernel):
    if len(img.shape) == 3 and img.shape[2] == 3:  # Color image
        h_img, w_img, _ = img.shape
        out = np.zeros((h_img-2, w_img-2), dtype=np.float64)
        new_img = np.zeros((h_img-2, w_img-2, 3))
        if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
            array = img[:, :, 0]
            for h in range(h_img-2):
                for w in range(w_img-2):
                    S = np.multiply(array[h:h+3, w:w+3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            for channel in range(3):
                new_img[:, :, channel] = out_
        else:
            for channel in range(3):
                array = img[:, :, channel]
                for h in range(h_img-2):
                    for w in range(w_img-2):
                        S = np.multiply(array[h:h+3, w:w+3], kernel)
                        out[h, w] = np.sum(S)
                out_ = np.clip(out, 0, 255)
                new_img[:, :, channel] = out_
        new_img = np.uint8(new_img)
        return new_img

    elif len(img.shape) == 2:  # Grayscale image
        h_img, w_img = img.shape
        out = np.zeros((h_img-2, w_img-2), dtype=np.float64)

        for h in range(h_img-2):
            for w in range(w_img-2):
                S = np.multiply(img[h:h+3, w:w+3], kernel)
                out[h, w] = np.sum(S)

        out_ = np.clip(out, 0, 255)
        new_img = np.uint8(out_)
        return new_img

    else:
        raise ValueError("Unsupported image format")


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)  
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :].flatten()
        data_g = Counter(g)
        plt.bar(list(data_g.keys()), data_g.values(), color='black')
        plt.savefig(f'static/img/grey_histogram.jpg', dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        data_rgb = [data_r, data_g, data_b]
        warna = ['red', 'green', 'blue']
        data_hist = list(zip(warna, data_rgb))
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f'{data[0]}')
            plt.savefig(f'static/img/{data[0]}_histogram.jpg', dpi=300)
            plt.clf()


def df(img):  # to make a histogram (count distribution frequency)
    values = [0]*256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1]+hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele*255/cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread('static\img\img_now.jpg', 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite('static/img/img_now.jpg', image_equalized)


def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    condition = np.logical_and(np.greater_equal(img_arr, lower_thres),
                               np.less_equal(img_arr, upper_thres))
    print(lower_thres, upper_thres)
    img_arr = np.asarray(img).copy()
    img_arr[condition] = 255
    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")

def create_puzzle(size):
    # Load the image
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)

    # Get image dimensions
    width, height = img.size

    # Calculate dimensions for each puzzle piece
    piece_width = width // size
    piece_height = height // size

    # Initialize an array to store the puzzle pieces
    puzzle_pieces = []

    for i in range(size):
        for j in range(size):
            # Crop a piece from the image
            left = j * piece_width
            upper = i * piece_height
            right = left + piece_width
            lower = upper + piece_height

            puzzle_piece = img.crop((left, upper, right, lower))
            puzzle_pieces.append(puzzle_piece)

            # Save the puzzle piece
            puzzle_piece.save(f"static/img/puzzle_piece_{i}_{j}.jpg")

    return puzzle_pieces

def create_random_puzzle(size):
    # Load the image
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)

    # Get image dimensions
    width, height = img.size

    # Calculate the total area of the original image
    original_area = width * height

    # Calculate the area of each puzzle piece
    piece_area = original_area / (size ** 2)

    # Calculate the side length of each puzzle piece
    piece_side_length = int(math.sqrt(piece_area))

    # Initialize an array to store the puzzle pieces
    puzzle_pieces = []

    for i in range(size):
        for j in range(size):
            # Crop a piece from the image
            left = j * piece_side_length
            upper = i * piece_side_length
            right = left + piece_side_length
            lower = upper + piece_side_length

            puzzle_piece = img.crop((left, upper, right, lower))
            puzzle_pieces.append(puzzle_piece)

    return puzzle_pieces


def randomize_puzzle_order(puzzle_pieces):
    # Shuffle the order of the puzzle pieces
    random.shuffle(puzzle_pieces)

def get_image_values(image_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        pixel_values = []

        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                pixel_values.append(pixel)

        return pixel_values, width, height
    except Exception as e:
        print(f"Error: {e}")
        return [], None, None
    
def zero_padding():
    img = cv2.imread("static/img/img_now.jpg")
    padded_img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    cv2.imwrite("static/img/img_now.jpg", padded_img)

def lowFilterPass():
    img = cv2.imread("static/img/img_now.jpg")
    # create the low pass filter
    lowFilter = np.ones((3,3),np.float32)/9
    # apply the low pass filter to the image
    lowFilterImage = cv2.filter2D(img,-1,lowFilter)
    cv2.imwrite("static/img/img_now.jpg", lowFilterImage)

def highFilterPass():
    img = cv2.imread("static/img/img_now.jpg")
    # create the high pass filter
    highFilter = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    # apply the high pass filter to the image
    highFilterImage = cv2.filter2D(img,-1,highFilter)
    cv2.imwrite("static/img/img_now.jpg", highFilterImage)

def bandFilterPass():
    img = cv2.imread("static/img/img_now.jpg")
    # create the band pass filter
    bandFilter = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    # apply the band pass filter to the image
    bandFilterImage = cv2.filter2D(img,-1,bandFilter)
    cv2.imwrite("static/img/img_now.jpg", bandFilterImage)

def newBlurring(size):
    img = cv2.imread("static/img/img_now.jpg")
    # create the band pass filter
    blur = cv2.blur(src=img, ksize=(size,size))
    cv2.imwrite("static/img/img_now.jpg", blur)

def gaussianBlur(size):
    img = cv2.imread("static/img/img_now.jpg")
    # create the band pass filter
    blur = cv2.GaussianBlur(src=img, ksize=(size,size),sigmaX=0)
    cv2.imwrite("static/img/img_now.jpg", blur)

def medianBlur(size):
    img = cv2.imread("static/img/img_now.jpg")
    # create the band pass filter
    blur = cv2.medianBlur(src=img, ksize=size)
    cv2.imwrite("static/img/img_now.jpg", blur)

def bilateral_filter():
    image = cv2.imread("static/img/img_now.jpg")
    cv_bilateral = cv2.bilateralFilter(image, 9, 75, 75)
    cv2.imwrite("static/img/img_now.jpg", cv_bilateral)

def lowpass_filter(size):
    image = cv2.imread("static/img/img_now.jpg")

    # Define kernel size and generate a random kernel
    kernel_size = size
    random_kernel = np.random.rand(kernel_size, kernel_size)
    random_kernel /= np.sum(random_kernel)  # Normalize the kernel

    cv_lowpass = cv2.filter2D(image, -1, random_kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_lowpass)

def highpass_filter(size):
    image = cv2.imread("static/img/img_now.jpg")

    # Define kernel size and generate a random kernel
    kernel_size = size
    random_kernel = np.random.randint(-1, 2, size=(kernel_size, kernel_size))
    random_kernel[1, 1] = (
        -np.sum(random_kernel) + 1
    )  # Adjust center element to make the sum zero

    cv_highpass = cv2.filter2D(image, -1, random_kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_highpass)

def bandpass_filter(size):
    image = cv2.imread("static/img/img_now.jpg")

    # Define kernel size and generate a random kernel
    kernel_size = size
    random_kernel = np.random.randint(-1, 2, size=(kernel_size, kernel_size))

    while np.sum(random_kernel) == 0:
        random_kernel = np.random.randint(-1, 2, size=(kernel_size, kernel_size))

    cv_bandpass = cv2.filter2D(image, -1, random_kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_bandpass)

# weeks 7 - ets 
def process_image():
    # Baca citra
    image = cv2.imread("static/img/img_now.jpg")

    # Daftar nama filter
    filter_names = [
        "Gaussian_Blur",
        "Median_Blur",
        "Bilateral_Filter",
        "Laplacian",
        "Sobel_X",
        "Sobel_Y",
        "Canny",
        "Sharpening",
        "Erosion",
        "Dilation",
        "Opening",
        "Closing",
        "Gradient",
        "TopHat"
    ]

    # Daftar hasil pemrosesan
    processed_images = []

    # Filter 1: Gaussian Blur
    gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
    processed_images.append(gaussian_blur)

    # Filter 2: Median Blur
    median_blur = cv2.medianBlur(image, 5)
    processed_images.append(median_blur)

    # Filter 3: Bilateral Filter
    bilateral_filter = cv2.bilateralFilter(image, 9, 75, 75)
    processed_images.append(bilateral_filter)

    # Filter 4: Laplacian
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    processed_images.append(laplacian)

    # Filter 5: Sobel X
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
    processed_images.append(sobel_x)

    # Filter 6: Sobel Y
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
    processed_images.append(sobel_y)

    # Filter 7: Canny Edge Detection
    canny = cv2.Canny(image, 100, 200)
    processed_images.append(canny)

    # Filter 8: Sharpening
    sharpening_kernel = np.array([[-1, -1, -1],
                                [-1, 9, -1],
                                [-1, -1, -1]])
    sharpened = cv2.filter2D(image, -1, sharpening_kernel)
    processed_images.append(sharpened)

    # Filter 9: Erosion
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(image, kernel, iterations=1)
    processed_images.append(erosion)

    # Filter 10: Dilation
    dilation = cv2.dilate(image, kernel, iterations=1)
    processed_images.append(dilation)

    # Filter 11: Opening (Erosion followed by Dilation)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    processed_images.append(opening)

    # Filter 12: Closing (Dilation followed by Erosion)
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    processed_images.append(closing)

    # Filter 13: Gradient (Dilation - Erosion)
    gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    processed_images.append(gradient)

    # Filter 14: Top Hat (Original - Opening)
    tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
    processed_images.append(tophat)

    # Simpan hasil pemrosesan ke berkas
    for i, processed_image in enumerate(processed_images):
        output_path = f"static/img/output_image_{i + 1}.jpg"
        cv2.imwrite(output_path, processed_image)

def get_duplicated_processed_images():
    processed_images = [str(i) for i in range(1, 15)]
    duplicated_images = []

    # Loop melalui nomor file dan menggandakan nama file yang sesuai formatnya
    for i in range(1, 15):
        file_name = f"static/img/output_image_{i}.jpg"
        duplicated_images.extend([file_name, file_name])

    random.shuffle(duplicated_images)  # Acak urutan hasil citra yang terduplikasi
    print(duplicated_images)
    return duplicated_images

# image_processing
def freeman_chain_code2(contour):
    chain_code = []
    prev_point = contour[0][0]
    
    for point in contour[1:]:
        x, y = point[0]
        dx = x - prev_point[0]
        dy = y - prev_point[1]
        
        # Calculate the angle in degrees
        angle = np.degrees(np.arctan2(dy, dx))
        
        # Convert the angle to Freeman Chain Code (numerical values)
        code = round((angle % 360) / 45) % 8
        chain_code.append(code)
        
        prev_point = point[0]
    
    return chain_code

def goofy(lst):
    # Add 1 to each element
    for i in range(len(lst)):
        lst[i] += 1
        # Check if any element becomes 10 and change it to 0
        if lst[i] == 10:
            lst[i] = 0

def create_image_from_chain_code(chain_code, image_size):
    # Initialize a white canvas
    image = np.zeros(image_size, dtype=np.uint8)
    x, y = image_size[0] // 2, image_size[1] // 2  # Start from the center

    # Define the Freeman Chain Code directional offsets
    offsets = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    for code in chain_code:
        dx, dy = offsets[code]
        x, y = x + dx, y + dy
        # Ensure the coordinates are within the image bounds
        x = max(0, min(x, image_size[0] - 1))
        y = max(0, min(y, image_size[1] - 1))
        # Set the pixel at the new position to white
        image[x, y] = 255

    return image

def read_binary(input_image_path):
    # Load the image
    image = cv2.imread(input_image_path)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    if image is None:
        print("Error: Unable to read the image.")
        return

    # Apply Otsu's thresholding
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    return binary_image

def get_contour(binary_image):
    
    contours, _ = cv2.findContours(
        binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

def FCC(binary_image):
    contours = get_contour(binary_image)
    for contour in contours:
        result = freeman_chain_code2(contour)
        print(f'result {result}')
        return result
        
def invert_binary_image(binary_image):
    # Invert the binary image using the NOT operation
    inverted_image = cv2.bitwise_not(binary_image)
    return inverted_image

def calculate_similarity(chain_code1, chain_code2):
    # Calculate the similarity between two FCCs
    length1 = len(chain_code1)
    length2 = len(chain_code2)

    # Pad the shorter chain code with zeros to match the length of the longer chain code
    if length1 < length2:
        chain_code1 = chain_code1 + [0] * (length2 - length1)
    elif length1 > length2:
        chain_code2 = chain_code2 + [0] * (length1 - length2)

    return np.sum(np.array(chain_code1) == np.array(chain_code2))

def recognize_digit(input_chain_code, knowledge_base):
    best_match = None
    best_similarity = 0

    for digit, data in knowledge_base.items():
        for stored_chain_code in data["FCC_8_Directions"]:
            for input_code in input_chain_code:
                similarity = calculate_similarity(input_code, stored_chain_code)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = digit

    return best_match

def number_recognition(image_path, knowledge_base):
    # Read and process the image
    binary_image = invert_binary_image(read_binary(image_path))
    contours = get_contour(binary_image)

    recognized_digits = []

    # Create a dictionary to map the position of contours to their FCC
    contour_position_mapping = {}

    for contour in contours:
        # Calculate FCC in 8 directions for each contour
        fcc_8_directions = freeman_chain_code2(contour)

        # Determine the position (e.g., x-coordinate) of the contour
        position = contour[0][0][0]  # Assuming x-coordinate is at index 0
        
        contour_position_mapping[position] = fcc_8_directions

    # Sort the contours based on their positions
    sorted_contours = sorted(contour_position_mapping.items())

    for _, fcc_8_directions in sorted_contours:
        recognized_digit = recognize_digit([fcc_8_directions], knowledge_base)

        if recognized_digit is not None:
            recognized_digits.append(recognized_digit)

    return recognized_digits