"""
This code was developed by the owner of the
"Tech with Tim" Youtube channel. I just wanted to share
the same information for the spanish community. You can
watch the original tutorial in the YouTube Channel 
"Tech with Tim".
"""

from turtle import width
import pygame
import os

pygame.font.init()
pygame.mixer.init()

# se crea la ventana con sus dimenciones 
WIDTH, HEIGHT = 900, 500   
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

# los colores necesarios para las balas letras y demas 
WHITE = (255, 255 , 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# el objeto con el cual colicionaran las naves y evitara que se salgan de la pantalla
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#efectos de sonido de los disparos 
BULLET_HIT_SOUND = pygame.mixer.Sound('Grenade.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Shot.wav')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#Fotogramas por segundo
FPS = 200
VEL = 3
BULLET_VEL = 10
MAX_BULLETS = 100

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 90, 70   

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#las diferentes imagenes que se mostraran para dal la imprecion de que la nave gira
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_yellow.png'))

YELLOW_SPACESHIP_R = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_U = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
YELLOW_SPACESHIP_L = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
YELLOW_SPACESHIP_D = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)


RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_red.png'))

RED_SPACESHIP_R = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_U = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
RED_SPACESHIP_L = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_D = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)

#la imagen de fondo del espacio 
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.png')), (WIDTH, HEIGHT))


#Esta función sirve para dibujar lo que necesitemos en la pantalla
#recive los vectores de direccion, los objetos naves,las vidas de los jugadores y las variables de direccion de las naves 
def draw_window(yellow_bulletsl, red_bulletsl, yellow_bulletsr, red_bulletsr, 
        yellow_bulletsu, red_bulletsu, yellow_bulletsd, red_bulletsd,
        red, yellow,red_health, yellow_health,dy,dr):
    #El orden en el que dibujamos las cosas importa
    #Si dibujas la spaceship antes que el fondo, la spaceship 
    #no se verá
    
    #mostrara la imgen del espacio de fondo
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    #mostrara las vidas de los jugadores
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    
    #dependiendo de la posicion segun la entrada por teclado mostrara una de las 4 imagenes de cada nave 
    #en el sentido de arriba, abajo, izquierda, derecha
    if dy == 0:
        WIN.blit(YELLOW_SPACESHIP_L, (yellow.x, yellow.y))    
    if dy == 1:
        WIN.blit(YELLOW_SPACESHIP_R, (yellow.x, yellow.y))
    if dy == 2:
        WIN.blit(YELLOW_SPACESHIP_U, (yellow.x, yellow.y))
    if dy == 3:
        WIN.blit(YELLOW_SPACESHIP_D, (yellow.x, yellow.y))

    if dr == 0:
        WIN.blit(RED_SPACESHIP_L, (red.x, red.y))   
    if dr == 1:
        WIN.blit(RED_SPACESHIP_R, (red.x, red.y))
    if dr == 2:
        WIN.blit(RED_SPACESHIP_U, (red.x, red.y))
    if dr == 3:
        WIN.blit(RED_SPACESHIP_D, (red.x, red.y))

    #mostrara la bala recorriendo su respectiva ruta en el mapa
    #
    if dy == 0:
        for bulletl in yellow_bulletsl:
            pygame.draw.rect(WIN, YELLOW, bulletl)  
    elif dy == 1:
        for bulletr in yellow_bulletsr:
            pygame.draw.rect(WIN, YELLOW, bulletr)
    elif dy == 2:
        for bulletu in yellow_bulletsu:
            pygame.draw.rect(WIN, YELLOW, bulletu)
    elif dy == 3:
        for bulletd in yellow_bulletsd:
            pygame.draw.rect(WIN, YELLOW, bulletd)

    if dr == 0:
        for bulletl in red_bulletsl:
            pygame.draw.rect(WIN, RED, bulletl) 
    if dr == 1:
        for bulletr in red_bulletsr:
            pygame.draw.rect(WIN, RED, bulletr)
    if dr == 2:
        for bulletu in red_bulletsu:
            pygame.draw.rect(WIN, RED, bulletu)
    if dr == 3:
        for bulletd in red_bulletsd:
            pygame.draw.rect(WIN, RED, bulletd)

    #Actualiza la pantalla
    pygame.display.update()

#esta funcion recive un objeto el cual se va mover en este caso nave amarrila, una orden de movimiento y una 
# variable que mostrara en que direccion quedo retornara la dirreccion en la que quedo
def yellow_handle_movement(keys_pressed, yellow,direccion):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
        direccion = 0
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
        direccion = 1
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
        direccion = 2
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
        yellow.y += VEL
        direccion = 3
    return direccion
    
#esta funcion recive un objeto el cual se va mover en este caso nave roja,una orden de movimiento y una 
# variable que mostrara en que direccion quedo retornara la dirreccion en la que quedo
def red_handle_movement(keys_pressed, red,direccion):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        red.x -= VEL
        direccion = 0    
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
        red.x += VEL
        direccion = 1 
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL
        direccion = 2 
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #DOWN
        red.y += VEL
        direccion = 3
    return direccion
    
    

#Esta función se encarga del movimiento de las balas, de la colisión de éstas
#y de eliminarlas cuando se salen de la pantalla
#resive los vectores por de las direcciones de las balas los objetos nave roja y amarilla 
#y la variable direccion
def handle_bullets(yellow_bulletsl, red_bulletsl, yellow_bulletsr, red_bulletsr, 
yellow_bulletsu, red_bulletsu, yellow_bulletsd, red_bulletsd, 
yellow, red,direcciony,direccionr):

    

    if  direcciony == 0:
        for bulletl in yellow_bulletsl:
            bulletl.x -= BULLET_VEL
            if bulletl.x < 0 and direcciony == 0:
                yellow_bulletsl.remove(bulletl)

    elif direcciony == 1:
        for bulletr in yellow_bulletsr:
            bulletr.x += BULLET_VEL
            if red.colliderect(bulletr):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bulletsr.remove(bulletr)
            elif bulletr.x > WIDTH and direcciony == 1:
                yellow_bulletsr.remove(bulletr)
                

    elif direcciony == 2:
        for bulletu in yellow_bulletsu:
            bulletu.y -= BULLET_VEL
            if bulletu.y > HEIGHT and direcciony == 2:
                yellow_bulletsu.remove(bulletu)

    elif direcciony == 3:
        for bulletd in yellow_bulletsd:
            bulletd.y += BULLET_VEL
            if bulletd.y < 0 and direcciony == 3:
                yellow_bulletsd.remove(bulletd)

            
    if  direccionr == 0:
        for bulletl in red_bulletsl:
            bulletl.x -= BULLET_VEL

            if yellow.colliderect(bulletl):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bulletsl.remove(bulletl)

            elif bulletl.x < 0 and direccionr == 0:
                red_bulletsr.remove(bulletl)

    elif direccionr == 1:
        for bulletr in red_bulletsr:
            bulletr.x += BULLET_VEL
            
            if bulletr.x > WIDTH and direccionr == 1:
                red_bulletsr.remove(bulletr)
                

    elif direccionr == 2:
        for bulletu in red_bulletsu:
            bulletu.y -= BULLET_VEL
            if bulletu.y > HEIGHT and direccionr == 2:
                red_bulletsu.remove(bulletu)

    elif direccionr == 3:
        for bulletd in red_bulletsd:
            bulletd.y += BULLET_VEL
            if bulletd.y < 0 and direccionr == 3:
                red_bulletsd.remove(bulletd)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 
                        2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


#Función principal
def main():
    direccionr =0
    direcciony =1
    #Estos rectángulos representan las spaceship
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    #vectores con los cuales las balas pueden recorrer el mapa
    red_bulletsr = []
    red_bulletsl = []
    red_bulletsu = []
    red_bulletsd = []

    yellow_bulletsr = []
    yellow_bulletsl = []
    yellow_bulletsu = []
    yellow_bulletsd = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        #Se encarga de que este bucle se repita 60 veces por segundo
        clock.tick(FPS)

        #pygame.event.get() es una lista con todos los eventos
        #de pygame. Con el bucle for la recorremos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #dependiendo de la posicion de la nave si recive una orden de disparar
            #generara una bala que se quedara en el vector dependiendo de la direccion y tomara su recorrido
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bulletsr) < MAX_BULLETS and direcciony == 1:
                    bulletl = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 5, 10, 5)
                    yellow_bulletsr.append(bulletl)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bulletsl) < MAX_BULLETS and direcciony == 0:
                    bulletr = pygame.Rect(yellow.x + yellow.width -100, yellow.y + yellow.height//2 + 5, 10, 5)
                    yellow_bulletsl.append(bulletr)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bulletsu) < MAX_BULLETS and direcciony == 2:
                    bulletu = pygame.Rect(yellow.x + yellow.width - 48, yellow.y + yellow.height//2 - 50, 5, 10)
                    yellow_bulletsu.append(bulletu)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bulletsd) < MAX_BULLETS and direcciony == 3:
                    bulletd = pygame.Rect(yellow.x + yellow.width - 48, yellow.y + yellow.height//2 + 40, 5, 10)
                    yellow_bulletsd.append(bulletd)
                    BULLET_FIRE_SOUND.play()
                
                #Se utilizan dos // en la división para que el resultado sea un número entero
                if event.key == pygame.K_RCTRL and len(red_bulletsl) < MAX_BULLETS and direccionr == 0:
                    bulletl = pygame.Rect(red.x + red.width -100, red.y + red.height//2 + 5, 10, 5)
                    red_bulletsl.append(bulletl)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bulletsr) < MAX_BULLETS and direccionr == 1:
                    bulletr = pygame.Rect(red.x + red.width, red.y + red.height//2 + 5, 10, 5)
                    red_bulletsr.append(bulletr)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bulletsu) < MAX_BULLETS and direccionr == 2:
                    bulletu = pygame.Rect(red.x + red.width - 48, red.y + red.height//2 - 50, 5, 10)
                    red_bulletsu.append(bulletu)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bulletsd) < MAX_BULLETS and direccionr == 3:
                    bulletd = pygame.Rect(red.x + red.width - 48, red.y + red.height//2 + 40, 5, 10)
                    red_bulletsd.append(bulletd)
                    BULLET_FIRE_SOUND.play()
                
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
  
        
        #Devuelve una lista con las teclas presionadas
        keys_pressed = pygame.key.get_pressed()
        
        direcciony=yellow_handle_movement(keys_pressed, yellow,direcciony)
        direccionr=red_handle_movement(keys_pressed, red,direccionr)
        
        handle_bullets(yellow_bulletsl, red_bulletsl, yellow_bulletsr, red_bulletsr, 
        yellow_bulletsu, red_bulletsu, yellow_bulletsd, red_bulletsd, 
        yellow, red,direcciony,direccionr)

        draw_window(yellow_bulletsl, red_bulletsl, yellow_bulletsr, red_bulletsr, 
        yellow_bulletsu, red_bulletsu, yellow_bulletsd, red_bulletsd,
        red, yellow,red_health, yellow_health,direcciony,direccionr)


    main()

#Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()