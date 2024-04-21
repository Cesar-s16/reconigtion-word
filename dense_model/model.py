from keras import layers, models
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from emnist import extract_training_samples, extract_test_samples

# Cargar y preparar el dataset EMNIST
train_images, train_labels = extract_training_samples('letters')
test_images, test_labels = extract_test_samples('letters')

# Convertir imágenes a secuencias de píxeles
train_sequences = [image.reshape((28, 28)).T.flatten() for image in train_images]
test_sequences = [image.reshape((28, 28)).T.flatten() for image in test_images]

# Pad secuencias para que tengan la misma longitud
train_sequences = pad_sequences(train_sequences, padding='post')
test_sequences = pad_sequences(test_sequences, padding='post')

# Convertir etiquetas a formato categórico
train_labels_cat = to_categorical(train_labels, num_classes=27)
test_labels_cat = to_categorical(test_labels, num_classes=27)

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
history = model.fit(train_sequences, train_labels_cat,
                    epochs=10,
                    batch_size=64,
                    validation_data=(test_sequences, test_labels_cat),
                    callbacks=[early_stopping])

# Guardar el modelo entrenado
model.save('letter_classifier.h5')
