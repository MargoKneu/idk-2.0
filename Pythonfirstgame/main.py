import pygame
import json

pygame.init()

width = 800
height = 800
tile_size = 40

game_over = 0
score = 0
lives = 3

clock = pygame.time.Clock()
fps = 60

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("first platformer")

bg_image = pygame.image.load("images/bg5.jpg")
bg_rect = bg_image.get_rect()

sound_jump = pygame.mixer.Sound("music/jump.wav")
sound_coin = pygame.mixer.Sound("music/coin.wav")
sound_game_over = pygame.mixer.Sound("music/game_over.wav")

with open("levels/map1.json", "r") as file:
    world_data = json.load(file)

map = 1
max_map = 4

def reset_level():
    player.rect.x = 100
    player.rect.y = height - 130
    lava_group.empty()
    exit_group.empty()
    with open(f"levels/map{map}.json", "r") as file:
        world_data = json.load(file)
        world = World(world_data)
        return world

def draw_text(text, color, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

class Player:
    def __init__(self):
        self.image_right = []
        self.image_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f"images/player{num}.png")
            img_right = pygame.transform.scale(img_right, (35, 70))
            img_left = pygame.transform.flip(img_right,True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)
        self.image = self.image_right[self.index]
        self.image = pygame.image.load("images/player1.png")
        self.image = pygame.transform.scale(self.image, (35,70))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 130
        self.gravity = 0
        self.jumped = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dead_image = pygame.image.load("images/ghost.png")

    def update(self):
        global game_over
        x = 0
        y = 0
        walk_speed = 10
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                print(1)
                self.jumped = True
                sound_jump.play()
            if key[pygame.K_a]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                x += 5
                self.direction = 1
                self.counter += 1
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.image_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                else:
                    self.image = self.image_left[self.index]
            self.gravity += 1
            y += self.gravity
            if self.gravity > 10:
                self.gravity = 0
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y,self.width, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False
                        print(self.jumped)
            self.rect.x += x
            self.rect.y += y

            if self.rect.bottom > height:
                self.rect.bottom = height
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
        elif game_over == -1:
            sound_game_over.play()
            self.image = self.dead_image
            if self.rect.y > 0:
                self.rect.y -= 5
        display.blit(self.image, self.rect)

bg_image = pygame.image.load("images/bg5.jpg")
bg_rect = bg_image.get_rect()

class World:
    def __init__(self, data):
        tile4_img = pygame.image.load("images/tile4.png")
        tile2_img = pygame. image.load("images/tile2.png")
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = { 1: tile4_img, 2: tile2_img}
                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                elif tile == 6:
                    coin = Coin(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pygame.image.load("images/tile5.png")
        self.image = pygame.transform.scale(image,(tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
lava_group = pygame.sprite.Group()

class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/door1.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

exit_group = pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/Bananas.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

coin_group = pygame.sprite.Group()

restart_button = Button (width // 2,height // 2, "images/restart_btn 6.png")
start_button = Button (width // 2 - 150,height // 2, "images/start_btn 6.png")
exit_button = Button (width // 2 + 150,height // 2, "images/exit_btn 4.png")

world = World(world_data)
player = Player()
run = True
main_menu = True
while run:
    display.blit(bg_image, bg_rect)
    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
            map = 1
            score = 0
            lives = 3
            world = reset_level()
    else:
        clock.tick(fps)
        player.update()
        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)
        coin_group.draw(display)
        draw_text(str(score), (255, 255, 255), 30, 10, 10)
        lava_group.update()
    if pygame.sprite.spritecollide(player, coin_group, True):
        sound_coin.play()
        score += 1
        print(score)
    if game_over == -1:
        if restart_button.draw():
            lives -= 1
            if lives == 0:
                main_menu = True
            player = Player()
            world = reset_level()
            game_over = 0
    if game_over == 1:
        game_over = 0
        if map < max_map:
            map += 1
            world = reset_level()
        else:
            print("win")
            main_menu = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
