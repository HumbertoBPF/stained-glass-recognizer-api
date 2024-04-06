import base64
import csv
import shelve

import cv2
import numpy as np
from skimage.feature import hog
from sklearn.neighbors import KNeighborsClassifier


def get_training_data():
    x = []

    my_shelf = shelve.open("training_data/HOG_training_data_all.out")

    for key in my_shelf:
        data = my_shelf[key]
        x.append(data)

    my_shelf.close()

    return np.array(x)


def get_image_labels():
    y_labels = []

    my_shelf = shelve.open("training_data/HOG_training_data_all.out")

    for key in my_shelf:
        y_labels.append(key)

    my_shelf.close()

    return np.array(y_labels)


def read_flask_image_file_with_open_cv(flask_image_file):
    file_str = flask_image_file.read()
    image_np_array = np.fromstring(file_str, np.uint8)
    return cv2.imdecode(image_np_array, cv2.IMREAD_UNCHANGED)


def get_input_data(input_image):
    window_size = 64
    resized_dim = (128 * 4, 128 * 4)

    x_input = []

    img = read_flask_image_file_with_open_cv(input_image)
    resized_img = cv2.resize(img, resized_dim)

    fd, _ = hog(
        resized_img,
        orientations=9,
        pixels_per_cell=(window_size, window_size),
        cells_per_block=(2, 2),
        visualize=True,
        channel_axis=-1
    )

    x_input.append(fd)

    return np.array(x_input)


def encode_image_in_base64(filename):
    with open(filename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def get_image_details(filename):
    with open('db_data/info_images.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["filename"] == filename:
                return {
                    "filename": row["filename"],
                    "image": encode_image_in_base64(f"db_data/images/{filename}"),
                    "artist": row["artist"],
                    "year_birth": row["year of birth"],
                    "year_passing": row["year of passing"],
                    "artist_reference": row["artist reference"],
                    "glass_date": row["glass date"],
                    "date_reference": row["date reference"],
                    "iconography": row["iconography"],
                    "church_name": row["church name"],
                    "url": row["url"]
                }

    return {}


def recognize_stained_glass(input_image):
    x = get_training_data()
    y_labels = get_image_labels()

    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(x, y_labels)

    x_input = get_input_data(input_image)

    y_predicted = classifier.predict(x_input)

    return get_image_details(f"{y_predicted[0]}.jpg")
