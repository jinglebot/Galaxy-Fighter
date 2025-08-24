import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Thanks to Driken5482 for 
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'retro-laser-2-236680.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'retro-laser-2-236680.mp3'))
    
HEALTH_FONT = pygame.font.SysFont('Arial', 40)
WINNER_FONT = pygame.font.SysFont('Comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','pixel_ship_yellow.png')) 
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','pixel_ship_red_small.png')) 
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.blit(SPACE, (0, 0))
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text,(10, 10))
    WIN.blit(yellow_health_text,(WIDTH - yellow_health_text.get_width() - 10, 10))

    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + red.width + VEL <= BORDER.x: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + red.height + VEL < HEIGHT - 15: # DOWN
        red.y += VEL

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + BORDER.width: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + yellow.width + VEL < WIDTH: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + yellow.height + VEL < HEIGHT - 15: # DOWN
        yellow.y += VEL

def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x < 0: 
            yellow_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    clock = pygame.time.Clock()
 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # SHOOTING
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # SCORING       
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # DECLARE WINNER
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
            winner_text = "RED WINS!"
            
        if winner_text != "":
            draw_winner(winner_text) # SOMEONE ALREADY WON
            break

        # SPACESHIP MOVEMENTS
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullets(red_bullets, yellow_bullets, red, yellow)

        draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
 
    main()

if __name__ == "__main__":
    main()
