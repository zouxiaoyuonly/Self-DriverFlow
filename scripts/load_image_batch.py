
# coding: utf-8

import scipy.misc
from sklearn.utils import shuffle
import numpy as np

from image_preprocess import process_image


INDEX_TRAIN_BATH = 0
INDEX_TEST_BATH = 0
DATASET_FOLDER_PATH = '../images/dataset_three_actions.csv'
IMAGES_FOLDER_PATH = '../images/images/'

# Image Algorithms Settings
KERNEL_SIZE = 3
LOW_THRESHOLD = 50
HIGH_THRESHOLD = 150

df_data = []
df_label = []

with open(DATASET_FOLDER_PATH, 'r') as file:
    i = 0
    for line in file:
        df_data.append(IMAGES_FOLDER_PATH + "image_" + str(i) + '.png')
        df_label.append(np.array(line.split(",")))
        i += 1

# Inputs
LIMIT = 1000

df_data, df_label = shuffle(df_data, df_label, random_state=22)
df_label = np.array(df_label, dtype=float)

X_train = df_data
X_test = X_train[LIMIT:]
X_train = X_train[:LIMIT]

# Outputs
Y_train = df_label
print(df_label.shape)
Y_test = Y_train[LIMIT:]
Y_train = Y_train[:LIMIT]

num_train_images = len(X_train)
num_test_images = len(X_test)

def get_train_batch(batch_size):
    global INDEX_TRAIN_BATH

    x_out = []
    y_out = []
    for i in range(0, batch_size):
        image = scipy.misc.imread(X_train[(INDEX_TRAIN_BATH + i) % num_train_images])
        image = process_image(image, KERNEL_SIZE, LOW_THRESHOLD, HIGH_THRESHOLD)
        scipy.misc.imsave("images_resized/test" + str(i) + ".png", (scipy.misc.imresize(image, [64, 224]) / 255.0))
        x_out.append(np.array(scipy.misc.imresize(image, [64, 224]) / 255.0).reshape(64, 224, 1))
        y_out.append(Y_train[(INDEX_TRAIN_BATH + i) % num_train_images])
    INDEX_TRAIN_BATH += batch_size
    return x_out, y_out


def get_test_batch(batch_size):
    global INDEX_TEST_BATH
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        image = scipy.misc.imread(X_test[(INDEX_TEST_BATH + i) % num_test_images])
        image = process_image(image, KERNEL_SIZE, LOW_THRESHOLD, HIGH_THRESHOLD)
        x_out.append(np.array(scipy.misc.imresize(image, [64, 224]) / 255.0).reshape(64, 224, 1))
        y_out.append(Y_test[(INDEX_TEST_BATH + i) % num_test_images])
    INDEX_TEST_BATH += batch_size
    return x_out, y_out
