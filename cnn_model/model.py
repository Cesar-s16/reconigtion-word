from keras import layers, models
from keras.preprocessing.image import ImageDataGenerator
from emnist import extract_training_samples, extract_test_samples

# Cargar y preparar el dataset EMNIST
train_images, train_labels = extract_training_samples('letters')
test_images, test_labels = extract_test_samples('letters')
train_images = train_images.reshape((train_images.shape[0], 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((test_images.shape[0], 28, 28, 1)).astype('float32') / 255

# Definir la arquitectura de la red
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1), padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(27, activation='softmax')  # 27 letras en el alfabeto inglés
])

# Compilar el modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Configurar el aumento de datos
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)

# Entrenar el modelo
model.fit(datagen.flow(train_images, train_labels, batch_size=64),
          epochs=10,  # Ajusta según sea necesario
          validation_data=(test_images, test_labels))

model.save('letter_classifier2.h5')
