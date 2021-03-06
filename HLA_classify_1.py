
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

from sklearn.cross_validation import StratifiedKFold


seed = 7
numpy.random.seed(seed)


dataset = numpy.loadtxt("HLA_B.csv", delimiter=",")

X = dataset[:,2:3356]
Y = dataset[:,0:1]

X_test = dataset[:,2:3356]
y_test = dataset[:,0:1]
X_train = dataset[:,2:3356]
y_train = dataset[:,0:1]

#import data set, first two columns designate output (allele group number) and 3353 numbers that represent sequence.

num_pixels = 3353


#reshape the sequences for input into NN
X_train = X_train.reshape(X_train.shape[0], 1, 1, 3353).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 1, 3353).astype('float32')

X_train = X_train / 4
X_test = X_test / 4
#normalize values corresponding to bases so that 0,1,2,3,4 are mapped to between [0,1]

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1] #should be two classes, either group 15 or 44


kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
cvscores = []
for train, test in kfold.split(X, Y):
	# create model
	model = Sequential()
	model.add(Convolution2D(32, 1, 1, border_mode='valid', input_shape=(1, 1, 3353), activation='relu')) #test 32 convolutional filters
	model.add(MaxPooling2D(pool_size=(1, 1)))
	model.add(Dropout(0.2)) #test dropout of 20% to prevent overfitting - prevent model from becoming specialized to training data, will need to test on different validation set later on
	model.add(Flatten()) #input currently treated as 2D, flatten to 1D vectors
	model.add(Dense(128, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	# compile 
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	# fit model
	model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=20, batch_size=300, verbose=2)
	scores = model.evaluate(X_test, y_test, verbose=0)
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
	cvscores.append(scores[1] * 100)
 
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))



