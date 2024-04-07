import csv
import os
import shelve

import cv2
from skimage.feature import hog

window_size = 64
resized_dim = (128 * 4, 128 * 4)
fd_hist = []
shelve_filename = "training_data/HOG_training_data_all.out"
reference_data_filename = "db_data/info_images.csv"
training_images_folder = "db_data/images"


def create_training_data():
    new_shelve_file = shelve.open(shelve_filename, 'n')
    new_shelve_file.close()

    shelve_file = shelve.open(shelve_filename)
    # Iterate over the files on the "images" folder
    for name in os.listdir(training_images_folder):
        with open(os.path.join(training_images_folder, name)) as f:
            print(f"Computing HOG features for image {name}")
            img = cv2.imread(f"{training_images_folder}/{name}")
            # Resizing image to make all the training images to have the same size
            resized_img = cv2.resize(img, resized_dim)
            # Computing HOG feature
            fd, hog_image = hog(
                resized_img,
                orientations=9,
                pixels_per_cell=(window_size, window_size),
                cells_per_block=(2, 2),
                visualize=True,
                channel_axis=-1
            )
            # Storing the image label (key) and the computed HOG feature (value)
            shelve_file[name] = fd

    shelve_file.close()


def create_reference_data():
    with open(reference_data_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        field = [
            "filename",
            "artist",
            "year of birth",
            "year of passing",
            "artist reference",
            "glass date",
            "date reference",
            "iconography",
            "church name",
            "url"
        ]

        writer.writerow(field)

        for name in os.listdir(training_images_folder):
            print(f"Adding record for {name} to the reference data CSV file")
            writer.writerow([name, "", "", "", "", "", "", "", "", ""])


create_training_data()
create_reference_data()
