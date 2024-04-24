import cv2
import numpy as np        
import math
from keras.models import load_model

# Cargar el modelo previamente entrenado
model = load_model('dense_model/letter_classifier.h5')

# Función para predecir el dígito basado en la imagen procesada
def predict_word(img):
    # Aplanar la imagen
    test_image = img.reshape(-1, 784)
    # Realizar la predicción y obtener el índice de la clase con mayor probabilidad
    return np.argmax(model.predict(test_image))

# Función para refinar cada letra de la imagen
def image_refiner(gray):
    org_size = 22
    img_size = 28
    rows, cols = gray.shape
    
    if rows > cols:
        factor = org_size / rows
        rows = org_size
        cols = int(round(cols * factor))        
    else:
        factor = org_size / cols
        cols = org_size
        rows = int(round(rows * factor))
    gray = cv2.resize(gray, (cols, rows))
    
    # Obtener padding 
    colsPadding = (int(math.ceil((img_size - cols) / 2.0)), int(math.floor((img_size - cols) / 2.0)))
    rowsPadding = (int(math.ceil((img_size - rows) / 2.0)), int(math.floor((img_size - rows) / 2.0)))
    
    # Aplicar padding 
    gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')
    return gray

def get_predict_word(path):
    img = cv2.imread(path, 0)

    ret, thresh = cv2.threshold(img, 127, 255, 0)

    # Obtener contornos
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # Ordenar los contornos por posición de izquierda a derecha
    contours_with_index = sorted(enumerate(contours), key=lambda x: cv2.boundingRect(x[1])[0])

    predicted_chars = ""
    for original_index, cnt in contours_with_index:
        x, y, w, h = cv2.boundingRect(cnt)

        if hierarchy[0][original_index][3] != -1 and w > 10 and h > 40:
            # Obtener ROI y refinar la imagen al tamaño 28x28
            roi = img[y:y+h, x:x+w]
            roi = cv2.bitwise_not(roi)
            roi = image_refiner(roi)
            
            # Determinar si se necesita aplicar espejo horizontal
            # Si la letra está más a la izquierda, no es necesario el espejo
            if x < img.shape[1] / 2:
                roi = cv2.flip(roi, 1)  # Espejo horizontal

            # Rotar la imagen si es necesario
            # Ejemplo de rotación de 90 grados hacia la izquierda
            roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Obtener predicción de la letra procesada
            pred = predict_word(roi)
            
            # Convertir la predicción en un carácter de ascii a caracter del alfabeto
            predicted_char = chr(pred + 65 - 1) if pred < 27 else None

            # Agregar el dígito a la cadena de letras predichos
            predicted_chars += predicted_char

    return predicted_chars
