import cv2
import numpy as np        
import math
from keras.models import load_model

# Cargar el modelo previamente entrenado
model = load_model('dense_model/letter_classifier_best.h5')

# Función para refinar cada letra de la imagen
def image_refiner(gray):
    org_size = 22
    img_size = 28
    rows, cols = gray.shape
    
    # Determinar la escala de factor
    if rows > cols:
        factor = org_size / rows
        rows, cols = org_size, int(round(cols * factor))
    else:
        factor = org_size / cols
        cols, rows = org_size, int(round(rows * factor))
      
    # Redimensionar la imagen  
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
    for original_index, contorno in contours_with_index:
        x, y, w, h = cv2.boundingRect(contorno)

        if hierarchy[0][original_index][3] != -1 and w > 10 and h > 40:
            # Obtener Imagen de zona de interes y refinar la imagen al tamaño 28x28
            image = image_refiner(cv2.bitwise_not(img[y:y+h, x:x+w]))
            
            # Determinar si se necesita aplicar espejo horizontal
            # Si la letra está más a la izquierda, no es necesario el espejo
            if x < img.shape[1]:
                image = cv2.flip(image, 1)  # Espejo horizontal

            # Rotar la imagen si es necesario
            # Ejemplo de rotación de 90 grados hacia la izquierda
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Obtener predicción de la letra procesada aplanando la imagen
            test_image = image.reshape(-1, 784)
            
            # Realizar la predicción y obtener el índice de la clase con mayor probabilidad
            pred = np.argmax(model.predict(test_image))
            
            # Convertir la predicción en un carácter de ascii a caracter del alfabeto
            predicted_char = chr(pred + 65 - 1) if pred < 27 else None

            # Agregar el dígito a la cadena de letras predichos
            predicted_chars += predicted_char

    return predicted_chars
