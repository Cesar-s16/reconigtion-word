import pygame
from  image_processor import get_predict_word

# Colores predefinidos, radio del bolígrafo y color de fondo
black = [0, 0, 0]
white = [255, 255, 255]
light_blue = (173, 216, 230)
draw_on = False
last_pos = (0, 0)
color = black  # Color inicial del bolígrafo
is_erasing = False  # Variable para indicar si se está borrando

# Tamaño de la pantalla
width = 750
height = 500

# Dimensiones del área negra
black_area_width = 500

# Dimensiones del área azul celeste
stripe_height = 140

# Cargar imágenes del lápiz y el borrador
lapiz_img = pygame.image.load("images/lapiz.png")
borrador_img = pygame.image.load("images/borrador.png")

# Inicializa el reloj de Pygame
clock = pygame.time.Clock()

# Pantalla de análisis
screen = pygame.display.set_mode((width+400, height))
screen.fill(white)
pygame.font.init()

# Fondo
UBUNTU = "assets/fonts/Ubuntu-BoldItalic.ttf"
font = pygame.font.Font(UBUNTU, 50)

# Dibujar el título sobre la pantalla
rect = pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
title = font.render("Tu palabra es:", True, white)
screen.blit(title, (width+50, height/4))

# Función para actualizar la imagen del marcador
def update_marker_img():
    global marker_img
    if is_erasing:
        marker_img = borrador_img
    else:
        marker_img = lapiz_img
        
# Muestra la predicción del número en la pantalla
def show_word_pred(predicted_text):
    font = pygame.font.Font(UBUNTU, 50)
    pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
    title = font.render("Tu palabra es:", True, white)
    screen.blit(title, (width+10, height/4))
    word = font.render(predicted_text, True, white)
    screen.blit(word, (width+40, height/2.5))

def crop(original): 
    # Dimensiones de las franjas azules a excluir
    exclude_height = 130

    # Coordenadas del área a recortar, excluyendo una porción más grande de las franjas azules
    crop_area = (0, exclude_height, width, height - 2 * exclude_height)
    
    # Crea una nueva superficie que es una subsuperficie de la original
    cropped = original.subsurface(crop_area)
    return cropped


# Esta función dibuja una línea redondeada entre dos puntos en una superficie pygame.
def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)

# Corremos la interfaz
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Manejar clics de botón "Predecir", "Limpiar" y "Borrador"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width + 50 <= event.pos[0] <= width + 200 and height - 100 <= event.pos[1] <= height - 50:
                    img = crop(screen)
                    pygame.image.save(img, "palabra.png")
                    predicted_word = get_predict_word("palabra.png")
                    print(predicted_word)
                    show_word_pred(predicted_word)

                elif width + 250 <= event.pos[0] <= width + 400 and height - 100 <= event.pos[1] <= height - 50:
                    font = pygame.font.Font(UBUNTU, 50)
                    screen.fill(white)
                    pygame.draw.rect(screen, black, [width, 0, black_area_width, height], 0)
                    title = font.render("Ingresa Palabra:", True, white)
                    screen.blit(title, (width+10, height/4))

                elif width + 250 <= event.pos[0] <= width + 400 and height - 200 <= event.pos[1] <= height - 150:
                    is_erasing = not is_erasing
                    update_marker_img()  # Actualizar la imagen del marcador

            if is_erasing:
                radius = 12 
                color = white 
            else:
                radius = 7 
                color = black 

            # Verificar si el evento del mouse está en el área de escritura
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] < width:
                if event.button == 1:
                    pygame.draw.circle(screen, color, event.pos, radius)
                    draw_on = True
            elif event.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            elif event.type == pygame.MOUSEMOTION:
                if draw_on and event.pos[0] < width:
                    pygame.draw.circle(screen, color, event.pos, radius)
                    roundline(screen, color, event.pos, last_pos, radius)
                last_pos = event.pos

        # Dibujar franjas azules celestes encima y debajo del área central de dibujo
        pygame.draw.rect(screen, light_blue, [0, 0, width, stripe_height])  # Franja superior
        pygame.draw.rect(screen, light_blue, [0, height - stripe_height, width, stripe_height])  # Franja inferior

        # Dibujar el título "PIZARRA" en la franja superior
        title_font = pygame.font.Font(UBUNTU, 100)
        title = title_font.render("PIZARRA", True, black)
        title_width = title.get_width()
        screen.blit(title, ((width - title_width) // 2, 10))  # Centrar el título horizontalmente en la franja superior

        # Mostrar el texto "Proyecto 1 IA" en la franja inferior
        font = pygame.font.Font(UBUNTU, 100)
        text = font.render("Proyecto 1 IA", True, black)
        text_rect = text.get_rect(center=(width // 2, height - stripe_height // 2))
        screen.blit(text, text_rect)

       # Dibujar botones
        pygame.draw.rect(screen, (150, 150, 150), (width+50, height-100, 150, 50))
        pygame.draw.rect(screen, (150, 150, 150), (width+250, height-100, 150, 50))
        pygame.draw.rect(screen, (150, 150, 150), (width+250, height-200, 150, 50))  # Botón Borrador
        font = pygame.font.Font(None, 36)
        text = font.render("Predecir", True, (255, 255, 255))
        screen.blit(text, (width+75, height-85))
        text = font.render("Limpiar", True, (255, 255, 255))
        screen.blit(text, (width+275, height-85))
        text = font.render("Borrador", True, (255, 255, 255))  # Texto del botón Borrador
        screen.blit(text, (width+260, height-185))  # Posición del texto del botón Borrador

        # Actualizar el mensaje del modo del marcador
        font = pygame.font.Font(UBUNTU, 50)
        mode = font.render("Modo:", True, white)
        screen.blit(mode, (width+10, 30))
        update_marker_img()
        screen.blit(marker_img, (width+165, 31))  # Posición de la imagen del marcador

        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    pygame.quit()