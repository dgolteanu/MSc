# This script was pulled from https://machinelearningmastery.com/tensorflow-tutorial-deep-learning-with-tf-keras/

# mlp for multiclass classification
from numpy import argmax
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
# load the dataset
path1 = '/Users/dolteanu/local_documents/Coding/MSc/MDGA/Data/800 SNP Calls.csv'
path2 = '/Users/dolteanu/local_documents/Coding/MSc/MDGA/Data/MLDSP_labels.csv'
df = read_csv(path1, header=0)
labels = read_csv(path2, header=0)
# split into input and output columns
X = df.T.values[:, :]
y= labels.values[:,19]
# ensure all data are floating point values
len(y)
print(X[0, :10])
x = X[1:,:]
len(x)
print(x[:2, :10])
X = x.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)
# split into train and test datasets

X_train, X_test, y_train, y_test = train_test_split(X, y)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
# determine the number of input features
n_features = X_train.shape[1]
print(n_features)
# define model
model = Sequential()
model.add(Dense(32, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(20, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(9, activation='softmax'))
# compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# fit the model
model.fit(X_train, y_train, epochs=150, batch_size=32, verbose=1)
# evaluate the model
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print('Test Accuracy: %.3f' % acc)
# make a prediction
row = [5.1,3.5,1.4,0.2]
yhat = model.predict([row])
print('Predicted: %s (class=%d)' % (yhat, argmax(yhat)))
