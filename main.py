import sys, pygame, time
pygame.init()

size=width,height=1280,720
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Chernobyl Simulator")
clock = pygame.time.Clock()
#napierdalasz sie z drugim ziomkiem
prev_time=time.time()
bg=90,90,90

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_r=pygame.image.load("img/bob/bob_r.png").convert_alpha()
        self.img_r=pygame.transform.scale(self.img_r,(100,130))

        self.img_l = pygame.image.load("img/bob/bob_l.png").convert_alpha()
        self.img_l = pygame.transform.scale(self.img_l, (100, 130))

        self.image=self.img_r
        self.rect = self.image.get_rect()
        self.right=True
        self.walking=False
        self.jumping=False
        self.now=0

        self.counter=0
        self.counter_skin=0
        self.counter_jump=0

        self.pressed_keys = {"left": False, "right": False}
        self.fire=False

        #walking sprites
        self.img_r_w1 = pygame.image.load("img/bob/bob_r_w1.png").convert_alpha()
        self.img_r_w1 = pygame.transform.scale(self.img_r_w1, (100, 130))

        self.img_r_w2 = pygame.image.load("img/bob/bob_r_w2.png").convert_alpha()
        self.img_r_w2 = pygame.transform.scale(self.img_r_w2, (100, 130))

        self.img_r_w3 = pygame.image.load("img/bob/bob_r_w3.png").convert_alpha()
        self.img_r_w3 = pygame.transform.scale(self.img_r_w3, (100, 130))

        self.img_l_w1 = pygame.image.load("img/bob/bob_l_w1.png").convert_alpha()
        self.img_l_w1 = pygame.transform.scale(self.img_l_w1, (100, 130))

        self.img_l_w2 = pygame.image.load("img/bob/bob_l_w2.png").convert_alpha()
        self.img_l_w2 = pygame.transform.scale(self.img_l_w2, (100, 130))

        self.img_l_w3 = pygame.image.load("img/bob/bob_l_w3.png").convert_alpha()
        self.img_l_w3 = pygame.transform.scale(self.img_l_w3, (100, 130))

        self.walking_right=[self.img_r_w1, self.img_r_w2, self.img_r_w3]
        self.walking_left = [self.img_l_w1, self.img_l_w2, self.img_l_w3]

    def animation_walking(self):
        self.counter+=250
        if self.counter%1250==0:
            if self.right:
                self.image=self.walking_right[self.counter_skin%3]
                self.counter_skin+=1

            else:
                self.image = self.walking_left[self.counter_skin%3]
                self.counter_skin += 1

    def walk(self):
        self.walking = True
        self.animation_walking()
        if self.right:
            self.rect.x += 500 * dt
        else:
            self.rect.x -= 500 * dt

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_r=pygame.image.load("img/items/ak47_r.png").convert_alpha()
        self.img_r=pygame.transform.scale(self.img_r,(120,40))

        self.img_l = pygame.image.load("img/items/ak47_l.png").convert_alpha()
        self.img_l = pygame.transform.scale(self.img_l, (120, 40))

        self.image = self.img_r
        self.rect = self.image.get_rect()
        self.counter=0

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img=pygame.image.load("img/items/bullet.png").convert_alpha()
        self.img=pygame.transform.scale(self.img,(20,20))

sprite_list = pygame.sprite.Group()

bob=Player()
bob.rect.x=100
bob.rect.y=100
sprite_list.add(bob)

#world

image_floor = pygame.image.load("img/world/floor.png").convert()
rect_floor = image_floor.get_rect()
rect_floor.x=0
rect_floor.y=520

#items
ak47=Gun()
ak47.rect.x=100
ak47.rect.y=470
sprite_list.add(ak47)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            #bob
            if event.key == pygame.K_a:
                bob.pressed_keys["left"] = True
            if event.key == pygame.K_d:
                bob.pressed_keys["right"] = True
            if event.key == pygame.K_SPACE:
                if bob.rect.y > 389:
                    bob.jumping = True
                    bob.counter_jump=0
            if event.key == pygame.K_f:
                bob.fire=True

        elif event.type == pygame.KEYUP:
            #bob
            if event.key == pygame.K_a:
                bob.pressed_keys["left"] = False
            if event.key == pygame.K_d:
                bob.pressed_keys["right"] = False
            if event.key == pygame.K_f:
                bob.fire=False

    bob.walking=False

    now = time.time()
    # delta time, movement not affected by fps
    dt = now - prev_time
    prev_time = now

    if bob.pressed_keys["left"] and bob.pressed_keys["right"]:
        bob.walking=False
    else:
        if bob.pressed_keys["left"]:
            bob.right = False
            bob.walk()

        if bob.pressed_keys["right"]:
            bob.right = True
            bob.walk()

    #bob gun
    if bob.fire:
        ak47.counter += 250
        if ak47.counter % 1250 == 0:
            print("i fire")

    if bob.walking==False:
        if bob.right:
            bob.image=bob.img_r
        else:
            bob.image=bob.img_l

    #gravity & jumping
    if bob.jumping:
        bob.counter_jump += 10
        bob.rect.y -= 500 * dt
        if bob.counter_jump > 200:
            bob.rect.y += 500 * dt
            if bob.rect.y < 389:
                bob.jumping = False
    else:
        if bob.rect.y < 390:
            bob.rect.y += 500 * dt

    #zrob animacje skakania

    #borders
    if bob.rect.x<0:
        bob.rect.x+=500*dt
    if bob.rect.x>1180:
        bob.rect.x-=500*dt

    #add a 2nd player controlled by wsad, 1v1 game

    ak47.rect.y=bob.rect.y+75
    if bob.right:
        ak47.image=ak47.img_r
        ak47.rect.x = bob.rect.x
    else:
        ak47.image=ak47.img_l
        ak47.rect.x = bob.rect.x-20

    clock.tick(75)
    screen.fill(bg)
    sprite_list.draw(screen)
    screen.blit(image_floor, rect_floor)
    pygame.display.flip()