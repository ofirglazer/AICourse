import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

# init
x = tf.constant(4)
print(x)
x = tf.constant(5, shape=(2,3,4))
print(x)
x = tf.random.uniform((5,4), minval=0, maxval=9)
print(x)

# keras
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(f"There are {x_train.shape[0]} data elements in the training dataset, each {x_train.shape[1]} X {x_train.shape[2]}")
x_train = x_train.reshape(-1, 28*28) #.astype("float32") / 255.0  # TODO leave as unint8
x_test = x_test.reshape(-1, 28*28) #.astype("float32") / 255.0  # TODO leave as unint8

# keras sequential API
print("Building a sequential model")
model = keras.Sequential(
    [
        keras.Input(shape=(28*28)),  # requires to print summary and build model before FIT
        layers.Dense(512, activation='relu'),  # fully connected layer
        layers.Dense(256, activation='relu'),
        layers.Dense(10)  # activation = softmax
    ]
)
print(model.summary())

print("Building a sequential model layer after layer")
model = keras.Sequential()
model.add(keras.Input(28*28))
print(model.summary())
model.add(layers.Dense(128, activation='relu'))
print(model.summary())
model.add(layers.Dense(128, activation='relu'))
print(model.summary())
model.add(layers.Dense(10))
print(model.summary())


model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=["accuracy"]
)

model.fit(x_train, y_train, batch_size=32, epochs=3) #, verbose=2)
model.evaluate(x_test, y_test, verbose=2)

# keras functional API
inputs = keras.Input(28*28, name='28*28_inputs')
x = layers.Dense(512, activation='relu', name='first_hidden_layer')(inputs)
x = layers.Dense(256, activation='relu', name='second_hidden_layer')(x)
outputs = layers.Dense(10, activation='softmax', name='output_layer')(x)
model = keras.Model(inputs=inputs, outputs=outputs)
print(model.summary())

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),  # logits not required due to softmax in outputs
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=["accuracy"]
)

model.fit(x_train, y_train, batch_size=32, epochs=3) #, verbose=2)
model.evaluate(x_test, y_test, verbose=2)
