import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile
import random

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


@app.route("/about")
@nocache
def about():
    return render_template('about.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("zoom.html", file_path="img/img_now.jpg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("zoom.html", file_path="img/img_now.jpg")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.jpg"])
    else:
        return render_template("histogram.html", file_paths=["img/red_histogram.jpg", "img/green_histogram.jpg", "img/blue_histogram.jpg"])


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form['lower_thres'])
    upper_thres = int(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/puzzle", methods=["POST"])
@nocache
def puzzle():
    num_puzzles = int(request.form['size'])
    image_path = "static/img/img_now.jpg"  # Assuming this is the path of your uploaded image
    rows = num_puzzles
    cols = num_puzzles

    parts = image_processing.create_puzzle(rows)

    if parts is not None:
        return render_template("puzzle.html", image_paths=[f"static/img/puzzle_piece_{i}_{j}.jpg" for i in range(rows) for j in range(cols)], rows=rows, cols=cols)
    else:
        return "Terjadi kesalahan saat membagi gambar. Silakan coba lagi."

@app.route("/random_puzzle", methods=["POST"])
@nocache
def random_puzzle():
    num_puzzles = int(request.form['size'])
    image_path = "static/img/img_now.jpg"  # Assuming this is the path of your uploaded image
    rows = num_puzzles
    cols = num_puzzles

    parts = image_processing.create_puzzle(rows)

    if parts is not None:
        return render_template("puzzle_random.html", image_paths=[f"static/img/puzzle_piece_{i}_{j}.jpg" for i in range(rows) for j in range(cols)], rows=rows, cols=cols)
    else:
        return "Terjadi kesalahan saat membagi gambar. Silakan coba lagi."

@app.route('/show_image_values', methods=['POST'])
@nocache
def show_image_values():
    # Mendapatkan nilai dari gambar
    pixel_values, width, height = image_processing.get_image_values('static/img/img_now.jpg')
    
    # Mengirimkan nilai-nilai tersebut ke template HTML
    return render_template("pixel_images.html", pixel_values=pixel_values, width=width, height=height)

@app.route("/zero_padding", methods=["POST"])
@nocache
def zero_padding():
    image_processing.zero_padding()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/lowFilterPass", methods=["POST"])
@nocache
def lowFilterPass():
    image_processing.lowFilterPass()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/highFilterPass", methods=["POST"])
@nocache
def highFilterPass():
    image_processing.highFilterPass()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/bandFilterPass", methods=["POST"])
@nocache
def bandFilterPass():
    image_processing.bandFilterPass()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/newBlurring", methods=["POST"])
@nocache
def newBlurring():
    newBlur = int(request.form['size'])
    image_processing.newBlurring(newBlur)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/gaussianBlur", methods=["POST"])
@nocache
def gaussianBlur():
    gaussianBlur = int(request.form['size'])
    image_processing.gaussianBlur(gaussianBlur)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/medianBlur", methods=["POST"])
@nocache
def medianBlur():
    medianBlur = int(request.form['size'])
    image_processing.medianBlur(medianBlur)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/bilateral_filter", methods=["POST"])
@nocache
def bilateral_filter():
    image_processing.bilateral_filter()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/lowpass_filter", methods=["POST"])
@nocache
def lowpass_filter():
    size = int(request.form["size"])
    image_processing.lowpass_filter(size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/highpass_filter", methods=["POST"])
@nocache
def highpass_filter():
    size = int(request.form["size"])
    image_processing.highpass_filter(size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/bandpass_filter", methods=["POST"])
@nocache
def bandpass_filter():
    size = int(request.form["size"])
    image_processing.bandpass_filter(size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")