import pygame

width = 800
height = 800

clock = pygame.time_Clock()
fps = 60

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("hero")

bg_image = pygame.image.load("images/bg5.jpg")
bg_rect = bg_image.get_rect()

class Hero:
    def __init__(self, name):
        self.name = name
        self.lives = 3
        self.level = 1

    def hello(self):
        print("hello")

hero1 = Hero("bear")
print(hero1.hello)

class Hero:
    def __init__(self):
        self.image = pygame.image.load("images/player1.png")
        self.image = pygame.transform.scale(self.image, (35,70))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 130

    def update(self):
        x = 0
        y = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            x -= 5
        if key[pygame.K_RIGHT]:
            y += 5
        self.rect.x += x
        self.rect.y += y
        display.blit(self.image, self.rect)

hero = Hero()

run = True
while run:
    clock.tick(fps)
    hero.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()