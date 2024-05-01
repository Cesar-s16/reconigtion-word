import tensorflow as tf
from keras import layers, models
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

try:
    # Intenta leer los archivos CSV desde la carpeta 'emnist' en la raíz del proyecto
    testing_letter = pd.read_csv('emnist/emnist-letters-test.csv')
    training_letter = pd.read_csv('emnist/emnist-letters-train.csv')
    print("Archivos CSV leídos correctamente.")
except FileNotFoundError:
    print("Error: No se encontraron los archivos CSV en la ubicación especificada.")

print(training_letter.shape)
print(testing_letter.shape)

#training_letters
y1 = np.array(training_letter.iloc[:,0].values)
x1 = np.array(training_letter.iloc[:,1:].values)
#testing_labels
y2 = np.array(testing_letter.iloc[:,0].values)
x2 = np.array(testing_letter.iloc[:,1:].values)

print(y1.shape)
print(x1.shape)

train_images = x1 / 255.0
test_images = x2 / 255.0

train_images = x1 / 255.0
test_images = x2 / 255.0

train_images_number = train_images.shape[0]
train_images_height = 28
train_images_width = 28
train_images_size = train_images_height*train_images_width

# Reshape y aplanar las imágenes de entrenamiento
train_images = train_images.reshape(train_images_number, train_images_height, train_images_width, 1)
train_images = train_images.reshape(train_images_number, -1)

test_images_number = test_images.shape[0]
test_images_height = 28
test_images_width = 28
test_images_size = test_images_height*test_images_width

# Reshape y aplanar las imágenes de prueba
test_images = test_images.reshape(test_images_number, test_images_height, test_images_width, 1)
test_images = test_images.reshape(test_images_number, -1)

number_of_classes = 27

y1 = tf.keras.utils.to_categorical(y1, number_of_classes)
y2 = tf.keras.utils.to_categorical(y2, number_of_classes)

train_x,test_x,train_y,test_y = train_test_split(train_images,y1,test_size=0.2,random_state = 42)

# Definir la arquitectura de la red
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(27, activation='softmax')  # 27 letras en el alfabeto inglés
])

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Añadir early stopping para evitar el sobreajuste
early_stopping = EarlyStopping(patience=3, restore_best_weights=True)

# Entrenar el modelo
history = model.fit(train_x, train_y,
                    epochs=10,
                    batch_size=64,
                    validation_data=(test_x, test_y),
                    callbacks=[early_stopping])

train_x2,test_x2,train_y2,test_y2 = train_test_split(train_images,y1,test_size=0.15,random_state = 42)


q = len(history.history['accuracy'])

plt.figsize=(10,10)
sns.lineplot(x = range(1,1+q),y = history.history['accuracy'], label='Accuracy')
sns.lineplot(x = range(1,1+q),y = history.history['val_accuracy'], label='Val_Accuracy')
plt.xlabel('epochs')
plt.ylabel('Accuray')

history1 = model.fit(train_x2,train_y2,epochs=10,validation_data=(test_x2,test_y2))

q = len(history1.history['accuracy'])

plt.figsize=(10,10)
sns.lineplot(x = range(1,1+q),y = history1.history['accuracy'], label='Accuracy')
sns.lineplot(x = range(1,1+q),y = history1.history['val_accuracy'], label='Val_Accuracy')
plt.xlabel('epochs')
plt.ylabel('Accuray')

# Guardar el modelo entrenado
model.save('letter_classifier_best.h5')