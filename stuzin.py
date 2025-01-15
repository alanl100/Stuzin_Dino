import pygame, random, sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()

FONT = pygame.font.Font(resource_path("images/opensans.ttf"), 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen_width, screen_height = 1300, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Mouse Game")

death_sound = pygame.mixer.Sound(resource_path('sounds/die-101soundboards.mp3'))
jump_sound = pygame.mixer.Sound(resource_path('sounds/jump-101soundboards.mp3'))
point_sound = pygame.mixer.Sound(resource_path('sounds/point-101soundboards.mp3'))

clock = pygame.time.Clock()
FPS = 60

classroom = pygame.image.load(resource_path("images/classroom.jpg")).convert()
classroom = pygame.transform.scale(classroom, (1300, 800))
mouse = pygame.image.load(resource_path("images/mouse.png")).convert_alpha()
mouse = pygame.transform.scale(mouse, (100, 100))
mouse_rect = mouse.get_rect(center=(50, 650))
rip = pygame.image.load(resource_path("images/rip.png")).convert_alpha()
rip = pygame.transform.scale(rip, (200, 200))
rip_rect = rip.get_rect(center=(650, 400))
trap = pygame.image.load(resource_path("images/mousetrap.png")).convert_alpha()
trap = pygame.transform.scale(trap, (100, 100))
floor = pygame.image.load(resource_path('images/floor.png')).convert()

mouse_x = 50
mouse_y = 650
mouse_vel_y = 0
gravity = 1
is_jumping = False

floor_xpos = 0
traps = []
score = 0

def get_scores_file_path():
    return resource_path('scores.txt')


with open(get_scores_file_path(), 'r') as file:
    highscore_file = file.read()

highscore = int(highscore_file)

def draw_floor():
    screen.blit(floor, (floor_xpos, 725))
    screen.blit(floor, (floor_xpos + 1300, 725))

def create_traps():
    num_traps = random.choice([1, 2, 3])  
    traps = []
    for i in range(num_traps):
        trap_rect = trap.get_rect(midtop=(1500 + i * 75, 650)) 
        trap_rect.width = 75 
        trap_rect.height = 75  
        traps.append(trap_rect)
    return traps

def move_traps(traps):
    for trap_rect in traps:
        trap_rect.x -= 9  
    traps = [trap for trap in traps if trap.right > 0]
    return traps

def draw_traps(traps):
    for trap_rect in traps:
        screen.blit(trap, trap_rect)

def check_collision(mouse_rect, traps):
    for trap_rect in traps:
        if mouse_rect.colliderect(trap_rect):
            death_sound.play()
            return False
    return True

def display_text(text, size, color, center):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def score_display(game_state):
    if game_state == 'main_game':
        score_text = FONT.render(str(int(score)), True, WHITE)
        screen.blit(score_text, (630, 10))
    elif game_state == 'game_over':
        display_text(f'Score: {int(score)}', 36, WHITE, (650, 100))
        display_text(f'High Score: {int(highscore)}', 36, WHITE, (650, 200))

def update_highscore(score, highscore):
    if score > highscore:
        highscore = score
    return highscore

def save_highscore(highscore):
    with open(get_scores_file_path(), 'w') as file:
        file.write(str(int(highscore)))

def main():
    global floor_xpos, traps, score, mouse_y, mouse_vel_y, is_jumping, highscore

    game_state = 'start'

    while True:
        screen.fill(WHITE)
        screen.blit(classroom, (0, 0))

        if game_state == 'start':
            display_text("The Mouse Game", 128, WHITE, (650, 150))
            display_text("Alan Liang and Naveed Razzaque", 32, WHITE, (650, 300))
            display_text("Press SPACE to Start", 48, WHITE, (650, 500))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = 'main_game'

        elif game_state == 'main_game':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping:
                    jump_sound.play()
                    mouse_vel_y = -25
                    is_jumping = True

            mouse_vel_y += gravity
            mouse_y += mouse_vel_y
            if mouse_y >= 650:
                mouse_y = 650
                is_jumping = False

            floor_xpos -= 9
            if floor_xpos <= -1300:
                floor_xpos = 0

            if not traps or traps[-1].x < 900:
                traps.extend(create_traps())
            traps = move_traps(traps)

            mouse_rect = pygame.Rect(mouse_x, mouse_y, mouse.get_width(), mouse.get_height())

            if not check_collision(mouse_rect, traps):
                game_state = 'game_over'
                save_highscore(highscore)

            score += .5
            if score > 0 and score % 500 == 0:
                point_sound.play()
            highscore = update_highscore(score, highscore)

            draw_floor()
            draw_traps(traps)
            screen.blit(mouse, mouse_rect)
            score_display('main_game')

            pygame.display.flip()
            clock.tick(FPS)

        elif game_state == 'game_over':
            display_text("GAME OVER", 64, WHITE, (650, 300))
            screen.blit(rip, (550, 400))
            score_display('game_over')
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    traps = []
                    score = 0
                    mouse_y = 650
                    mouse_vel_y = 0
                    game_state = 'main_game'

if __name__ == "__main__":
    main()
