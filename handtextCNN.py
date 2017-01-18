


import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')

seed = 7
numpy.random.seed(seed)


dataset = numpy.loadtxt("letterTrain1.csv", delimiter=",")

X_test = dataset[:,1:17]
y_test = dataset[:,0]
X_train = dataset[:,1:17]
y_train = dataset[:,0]


num_pixels = 16

X_train = X_train.reshape(X_train.shape[0], 1, 1, 16).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 1, 16).astype('float32')

X_train = X_train / 15
X_test = X_test / 15

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]


def baseline_model():
	# create model
	model = Sequential()
	model.add(Convolution2D(32, 1, 1, border_mode='valid', input_shape=(1, 1, 16), activation='relu'))
	model.add(MaxPooling2D(pool_size=(1, 1)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	# compile 
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model


# build model
model = baseline_model()
# fit model
model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=100, batch_size=300, verbose=2)
# evaluate
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))