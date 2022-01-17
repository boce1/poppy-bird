import pygame
import random

pygame.init()
pygame.mixer.init()


WHITE = (255,255,255)
BLACK = (0,0,0)
BROWN = (237, 192, 168)
BLACK_BROWN = (59, 28, 8)
speed_background_and_pipes = 5

font = pygame.font.SysFont("Consolas", 100, italic=True)
BACKGROUND = pygame.image.load("images\\background.png")
player = (pygame.image.load("images\\poop.png"), pygame.image.load("images\\poop2.png"))
particles_ = (pygame.image.load("images\\particles.png"), pygame.image.load("images\\particles2.png"))

dead_sound = pygame.mixer.Sound("audio\\dead.wav")
fart_sound = pygame.mixer.Sound("audio\\fart.wav")

WIDTH = BACKGROUND.get_width()
HEIGHT = BACKGROUND.get_height()

pygame.display.set_caption('Flappy Bird')
window = pygame.display.set_mode((WIDTH, HEIGHT))


class Pipe:
    def __init__(self):
        self.width = 50
        self.hole = 200
        self.minimum_size = 100
        self.top = random.randint(self.minimum_size, HEIGHT - self.hole - self.minimum_size) 
        self.bottom = self.top + self.hole
        self.x = WIDTH - self.width
        self.speed = speed_background_and_pipes

    def draw(self):
        distance_brown_black_rect = 10
        self.x -= self.speed
        pygame.draw.rect(window, BLACK, (self.x, 0, self.width, self.top), 2)
        pygame.draw.rect(window, BLACK, (self.x, self.bottom, self.width, HEIGHT - self.top - self.hole), 2)
        pygame.draw.rect(window, BLACK_BROWN, (self.x, 0, self.width, self.top), 1)
        pygame.draw.rect(window, BLACK_BROWN, (self.x, self.bottom, self.width, HEIGHT - self.top - self.hole), 1)    

        pygame.draw.rect(window, BLACK, (self.x + distance_brown_black_rect, distance_brown_black_rect, self.width - 2*distance_brown_black_rect, self.top - 2*distance_brown_black_rect), 2)
        pygame.draw.rect(window, BLACK, (self.x + distance_brown_black_rect, self.bottom + distance_brown_black_rect, self.width - 2*distance_brown_black_rect, HEIGHT - self.top - self.hole - 2*distance_brown_black_rect), 2)
        pygame.draw.rect(window, BROWN, (self.x + distance_brown_black_rect, distance_brown_black_rect, self.width - 2*distance_brown_black_rect, self.top - 2*distance_brown_black_rect))
        pygame.draw.rect(window, BROWN, (self.x + distance_brown_black_rect, self.bottom + distance_brown_black_rect, self.width - 2*distance_brown_black_rect, HEIGHT - self.top - self.hole - 2*distance_brown_black_rect))

pipes = [Pipe()]

class Bird:
    #nesto = 0
    def __init__(self, width, height, image, particle_image):
        self.particle_image = particle_image
        self.image = image
        self.width = width
        self.height = height
        self.x = 100
        self.y = WIDTH // 2 - self.width // 2
        self.velocity = 0
        self.gravity = 1
        self.up_force = 15
        self.score = 0

    def is_dead(self, pipes_arr):
        if self.y <= -self.height or self.y >= HEIGHT + self.height:
            return True
        for i in range(len(pipes_arr) - 2):
            if pipes_arr[i].x - self.width <= self.x <= pipes_arr[i].x + pipes_arr[i].width:
                if self.y <= pipes_arr[i].top or self.y >= pipes_arr[i].bottom - self.height:
                    return True
        return False

    def go_down(self):
        global pipes, main_screen
        self.velocity += self.gravity
        self.y += self.velocity
        if self.is_dead(pipes):
            self.velocity = 0
            self.y = HEIGHT // 2 - self.height // 2
            pygame.mixer.Sound.play(dead_sound)
            pipes = [Pipe()]
            self.score = 0
            pygame.time.wait(100)
            main_screen = True

    def draw(self):
        if self.velocity > 0:
            window.blit(self.image[0], (self.x, self.y))
        else:
            window.blit(self.image[1], (self.x, self.y))
            if self.velocity % 2 == 0:
                window.blit(self.particle_image[0], ((self.x + self.width // 2) - self.particle_image[0].get_width() // 2, self.y + self.height))
            else:
                window.blit(self.particle_image[1], ((self.x + self.width // 2) - self.particle_image[1].get_width() // 2, self.y + self.height))
        self.go_down()

    def jump(self, key_event):
        if (key_event.type == pygame.KEYDOWN and key_event.key in (pygame.K_SPACE, pygame.K_UP)) or \
            (key_event.type == pygame.MOUSEBUTTONDOWN and key_event.button == 1):
            self.velocity = -self.up_force
            pygame.mixer.Sound.play(fart_sound)

b = Bird(player[0].get_width(),player[0].get_height(), player, particles_)

def show_points():
    message = font.render(f"{b.score}", BLACK_BROWN, True)
    window.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))

def is_point(i):
    if b.x == pipes[i].x + pipes[i].width // 2 - pipes[i].width//2:
        b.score += 1

def add_pipes(i):
    global pipes
    distance_of_spawaning = 7 * WIDTH // 10
    if pipes[i].x == distance_of_spawaning:
        pipes.append(Pipe())
    if i > 0 and pipes[i - 1].x == -pipes[i-1].width:
        pipes.pop(i - 1)


x_of_1st = 0 # background
x_of_2nd = WIDTH
def draw_background(speed):
    global x_of_1st, x_of_2nd
    x_of_1st -= speed_background_and_pipes
    x_of_2nd -= speed_background_and_pipes
    if x_of_1st <= -WIDTH:
        x_of_1st = WIDTH
    if x_of_2nd <= -WIDTH:
        x_of_2nd = WIDTH
    window.blit(BACKGROUND, (x_of_1st, 0))
    window.blit(BACKGROUND, (x_of_2nd, 0))


def main():
    draw_background(speed_background_and_pipes)
    for index, pipe in enumerate(pipes):
        pipe.draw()
        add_pipes(index)
        is_point(index)
    #add_pipes()
    show_points()
    b.draw()
    pygame.display.update()


def main_menu():
    global main_screen, run
    while main_screen:
        clock.tick(60)
        draw_background(speed_background_and_pipes)
        message = font.render("Press any key", BLACK_BROWN, True)
        window.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_screen = False
                run = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                main_screen = False
        continue

clock = pygame.time.Clock()
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load('audio\\music.wav')
pygame.mixer.music.play(-1)
main_screen = True
run = True
while run:
    clock.tick(60)
    main_menu()
    main()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        b.jump(event)
pygame.quit()    
