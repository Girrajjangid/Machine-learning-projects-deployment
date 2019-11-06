import warnings
warnings.filterwarnings('ignore')
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import math

import tensorflow.keras
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Sequential

train_dir = 'dataset/train/'
test_dir = 'dataset/validate/'

n_train = 8000
n_test = 2000
input_shape = (200,200, 3)
batch_size = 32
epochs = 5

train_data_generator = ImageDataGenerator(rescale=1./255)
test_data_generator  = ImageDataGenerator(rescale=1./255)
train_generator = train_data_generator.flow_from_directory(train_dir,
                                                          target_size=(200,200),
                                                          batch_size=batch_size,
                                                          class_mode='categorical')

test_generator = test_data_generator.flow_from_directory(test_dir,
                                                          target_size=(200,200),
                                                          batch_size=batch_size,
                                                          class_mode='categorical')
labels_dictionary = train_generator.class_indices
labels_name = list(labels_dictionary.keys())
n_labels = len(labels_name)

def create_model():
    model = Sequential()                                                                           
    model.add(Conv2D(filters=16, kernel_size=(3,3), activation='relu', padding='same', input_shape=input_shape))
    model.add(Conv2D(filters=16, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D())
    model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D())
   	model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D())
    model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D())
    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(10, activation='sigmoid'))
    return model

model = create_model()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("Model created.")
model.summary()

def get_path_of_imgs(labels, directory):
    class_paths = {}
    for each_label in labels:
        image_paths = np.array([])
        class_path = os.path.join(directory, each_label)
        images = os.listdir(class_path)
        for image in images:
            image_path = os.path.join(class_path, image)
            image_paths = np.append(image_paths, image_path)
        class_paths[each_label] = image_paths        
    return class_paths

img_path_of_train = get_path_of_imgs(labels_name, train_dir)
img_path_of_test  = get_path_of_imgs(labels_name, test_dir)

tensorboard = TensorBoard(log_dir='logs/')
print('Training starts.')
model.fit_generator(train_generator,
                    steps_per_epoch = math.floor(n_train/batch_size),
                    validation_data=test_generator,
                    validation_steps=math.floor(n_test/batch_size),
                    epochs=epochs,
                    callbacks=[tensorboard])          
model.save('model.h5')
print('Model successfully saved.')