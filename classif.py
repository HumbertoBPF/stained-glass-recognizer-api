import base64
import shelve

import boto3
import cv2
import numpy as np
from skimage.feature import hog
from sklearn.neighbors import KNeighborsClassifier


def get_training_data(my_shelf):
    x = []

    for key in my_shelf:
        data = my_shelf[key]
        x.append(data)

    return np.array(x)


def get_image_labels(my_shelf):
    y_labels = []

    for key in my_shelf:
        y_labels.append(key)

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
    client_dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    response = client_dynamodb.get_item(
        Key={
            'name': {
                'S': filename,
            },
        },
        TableName='stained-glass-images',
    )

    item = response.get("Item", {})

    client_s3 = boto3.client('s3', region_name='us-east-1')

    output_image = client_s3.get_object(
        Bucket='stained-glass-images',
        Key=item["name"]["S"],
    )

    return {
        "filename": item["name"]["S"],
        "image": base64.b64encode(output_image["Body"].read()).decode(),
        "artist": item["artist"]["S"],
        "year_birth": item["year_birth"]["S"],
        "year_passing": item["year_passing"]["S"],
        "artist_reference": item["artist_reference"]["S"],
        "glass_date": item["glass_date"]["S"],
        "date_reference": item["date_reference"]["S"],
        "iconography": item["iconography"]["S"],
        "church_name": item["church_name"]["S"],
        "url": item["url"]["S"]
    }


def recognize_stained_glass(input_image):
    my_shelf = shelve.open("training_data/HOG_training_data_all.out")

    x = get_training_data(my_shelf)
    y_labels = get_image_labels(my_shelf)

    my_shelf.close()

    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(x, y_labels)

    x_input = get_input_data(input_image)

    y_predicted = classifier.predict(x_input)

    return get_image_details(f"{y_predicted[0]}.jpg")
