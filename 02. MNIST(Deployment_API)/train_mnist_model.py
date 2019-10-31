import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib

mnist = input_data.read_data_sets("MNIST_data")
X_train, X_test, y_train, y_test  = mnist.train.images , mnist.test.images, mnist.train.labels, mnist.test.labels

shuffle_index = np.random.permutation(X_train.shape[0])
X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]

# Train SGDClassifier
sgd_clf = SGDClassifier(random_state=42, max_iter=10)
sgd_clf.fit(X_train, y_train)

print("Model trained.")
print("Accuracy: ",sgd_clf.score(X_test,y_test),"%")

# Dump the model to the file
joblib.dump(sgd_clf, "mnist_model.pkl")
