import pygame
from  process_image import get_predict_num

# pre defined colors, pen radius and font color
black = [0, 0, 0]
white = [255, 255, 255]
draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 7
font_size = 500

# Screen size
width = 640
height = 400

# Final text of prediction
final_text = ""

# Initializing screen
screen = pygame.display.set_mode((width+400, height))
screen.fill(white)
pygame.font.init()

# Font
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
font = pygame.font.Font(OPEN_SANS, 36)

# Draw the title onto the screen
rect = pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
title = font.render("Tu palabra es:", True, white)
screen.blit(title, (width+50, height/4))

# Display the number prediction on to the screen
def show_number_pred():
    pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
    title = font.render("Tu palabra es:", True, white)
    screen.blit(title, (width+10, height/4))
    number = font.render(final_text, True, white)
    screen.blit(number, (width+50, height/2.5))


def crope(orginal):
    cropped = pygame.Surface((width-5, height-5))
    cropped.blit(orginal, (0, 0), (0, 0, width-5, height-5))
    return cropped


def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)


try:
    while True:

        # Game Events
        e = pygame.event.wait()

        # Clear screen after right click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button == 3):
            screen.fill(white)
            pygame.draw.rect(screen, black, [width+2, 0, 400, height], 0)
            title = font.render("Ingresa Palabra:", True, white)
            screen.blit(title, (width+10, height/4))

        # Quit Game
        if e.type == pygame.QUIT:
            raise StopIteration

        # Start drawing after left click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button != 3):
            color = black
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True

        # Stop drawing after releasing left click
        if e.type == pygame.MOUSEBUTTONUP and e.button != 3:
            draw_on = False
            fname = "screenshot.png"
            img = crope(screen)
            pygame.image.save(img, fname)

            predicted_text = get_predict_num(fname)
            final_text = predicted_text
            print(predicted_text)
            show_number_pred()

        # start drawing line on screen if draw is true
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos

        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()
