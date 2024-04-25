import pygame
from  process_image import get_predict_word

# Colores predefinidos, radio del bolígrafo y color de fondo
black = [0, 0, 0]
white = [255, 255, 255]
draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 7
font_size = 500

# Tamaño de la pantalla
width = 640
height = 400

# Inicializa el reloj de Pygame
clock = pygame.time.Clock()

# Pantalla de análisis
screen = pygame.display.set_mode((width+400, height))
screen.fill(white)
pygame.font.init()

# Fondo
UBUNTU = "assets/fonts/Ubuntu-BoldItalic.ttf"
font = pygame.font.Font(UBUNTU, 36)

# Dibujar el título sobre la pantalla
rect = pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
title = font.render("Tu palabra es:", True, white)
screen.blit(title, (width+50, height/4))

# Muestra la predicción del número en la pantalla
def show_word_pred(predicted_text):
    pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
    title = font.render("Tu palabra es:", True, white)
    screen.blit(title, (width+10, height/4))
    word = font.render(predicted_text, True, white)
    screen.blit(word, (width+50, height/2.5))

# Recorta la superficie de la imagen
def crop(original):
    # Crea una nueva superficie que es una subsuperficie de la original
    cropped = original.subsurface((0, 0, width-5, height-5))
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

            # Manejar clics de botón "Predecir" y "Limpiar"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en el botón "Predecir"
                if width + 50 <= event.pos[0] <= width + 200 and height - 100 <= event.pos[1] <= height - 50:
                    fname = "palabra.png"
                    img = crop(screen)
                    pygame.image.save(img, fname)
                    predicted_word = get_predict_word(fname)
                    print(predicted_word)
                    show_word_pred(predicted_word)

                # Verificar si se hizo clic en el botón "Limpiar"
                elif width + 250 <= event.pos[0] <= width + 400 and height - 100 <= event.pos[1] <= height - 50:
                    screen.fill(white)
                    pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
                    title = font.render("Ingresa Palabra:", True, white)
                    screen.blit(title, (width+10, height/4))

            # Empieza a dibujar al hacer clic en el click izquierdo
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = black
                pygame.draw.circle(screen, color, event.pos, radius)
                draw_on = True
            # Para de dibujar después de soltar el clic izquierdo
            elif event.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            # Inicia el dibujo de la línea en la pantalla si draw_on es verdadero
            elif event.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, color, event.pos, radius)
                    roundline(screen, color, event.pos, last_pos, radius)
                last_pos = event.pos


        # Dibujar botones
        pygame.draw.rect(screen, (150, 150, 150), (width+50, height-100, 150, 50))
        pygame.draw.rect(screen, (150, 150, 150), (width+250, height-100, 150, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("Predecir", True, (255, 255, 255))
        screen.blit(text, (width+75, height-85))
        text = font.render("Limpiar", True, (255, 255, 255))
        screen.blit(text, (width+275, height-85))

        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    pygame.quit()