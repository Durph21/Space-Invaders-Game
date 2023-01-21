###############################################
###############################################

#Intermediate programming - CA2 - DM - 121494462

################################################
################################################


#---Space invaders game---#
#can move player, shoot, there are enemies, who shoot back. 
#enemies move left to right and come down the screen.
#player must destroy all enemies to progress to a higher difficulty
#if player loses all their lives they lose
#they can destroy enemies by shooting them
#player has 3 lives, if shot by enemy, lose 1 life.
#health resets at each level


#imports etc
import sys, pygame, random
from random import choice
import math
from pygame import mixer
pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group() 
rocket_group = pygame.sprite.Group()

#fonts
font1 = pygame.font.SysFont('Constantia', 25)
font2 = pygame.font.SysFont('Constantia', 50)
font3 = pygame.font.SysFont('Constantia', 35)

#sounds
gun_fx = pygame.mixer.Sound("laser.mp3")
gun_fx.set_volume(0.5)

#color and size
size = width, height = 1080, 750
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
screen = pygame.display.set_mode(size)

#time
last_shot = pygame.time.get_ticks()
cool_down = 450 #milliseconds           ########################
last_count = pygame.time.get_ticks()

#variables
end_game = 1
score = 0

#myGame class - contains main functions to run out game
class myGame(pygame.sprite.Sprite):
    def __init__(self) -> None:
        
        #set init variables
        self.countdown = 3
        self.clock = pygame.time.Clock()
        self.fps = 24

        #rows and cols for enemy spawn
        self.rows = 4
        self.cols = 9

        #screen
        self.black = 0, 0, 0
        pygame.display.set_caption("Space Invaders")
        self.back_ground = pygame.image.load('space.webp').convert()

        #player
        self.game_over = 0
        

        self.last_count = pygame.time.get_ticks()
        #rocket
        # self.rocket_image = pygame.image.load("rocket.png")
        
        self.rocket_view = RocketState(player_view.player_x_pos,  player_view.player_y_pos)

        #enemies
        self.enemy_cooldown = 2000
        self.last_enemy_shot = pygame.time.get_ticks()
        self.move_num = 100
        
        #when the frame rate drops, due to computer performance, the enemy shooting will slow and allow it to recover
        if self.fps < 24:
            self.enemy_cooldown = 4000

    #create enemy function
    #loops through rows and cols to make field of 45 enemies, that number set above
    def create_enemy(self):
        for row in range(self.rows):
                for item in range(self.cols):
                    enemy = enemies(135 + item * 100, self.move_num + row * 65) 
                    enemy_group.add(enemy)
        
    #function to draw text on the screen such as score and win/lose
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #main, run game function
    def run_game(self):
        
        #get ticks to keep track of time, used for different things.
        self.clock.tick(self.fps)

        #call create enemy function
        self.create_enemy() 

        #While true,
        #used to actually 'run' the game
        while True:
            time_now = pygame.time.get_ticks()
            for event in pygame.event.get():
                pygame.display.update()
                
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pass

            #write to screen
            #what certain objects are to be displayed
            if player_view.player_x_pos + player_view.playerchange > 0 and player_view.player_x_pos + player_view.playerchange < width - 108:
                player_view.player_x_pos += player_view.playerchange
                screen.blit(self.back_ground, (0, 0))

                # screen.blit(player_image, (player_view.player_x_pos, player_view.player_y_pos))
                #further, draw function
                rocket_group.draw(screen)
                enemy_group.draw(screen)
                player_group.draw(screen)
                bullet_group.draw(screen)

            #when player has destroyed all the enemies, we want to rerun and spawn more enemies,
            #however, we also increase then difficulty for the user, by checking score
            if len(enemy_group) == 0:
                #game difficulty increases
                #score display goes up
                if RocketState.score > 3000:
                    myGame.create_enemy(self)
                    enemies.move_down += 7
                    PlayerState.level = 2
                    #health reset
                    player_view.health_left = 3
                if RocketState.score > 6000:
                    myGame.create_enemy(self)
                    enemies.move_down += 7
                    PlayerState.level = 3
                    #health reset
                    player_view.health_left = 3
                if RocketState.score > 9000:
                    myGame.create_enemy(self)
                    enemies.move_down += 7
                    PlayerState.level =4
                    #health reset
                    player_view.health_left = 3
                if RocketState.score > 12000:
                    myGame.create_enemy(self)
                    enemies.move_down += 7
                    PlayerState.level = 5
                    #health reset
                    player_view.health_left = 3
                if RocketState.score > 15200:
                    myGame.create_enemy(self)
                    enemies.move_down += 7
                    PlayerState.level = 6
                    #health reset
                    player_view.health_left = 3
            
            #count down to begin the game must reach 0 before its starts
            if self.countdown == 0:
                my_game.draw_text("Score: {}".format(RocketState.score), font3, white, 45, 15)
                my_game.draw_text("Level: {}".format(PlayerState.level), font3, white, 250, 15)
                if time_now - self.last_enemy_shot > self.enemy_cooldown and len(enemy_group) > 0:
                    attacking_enemy = random.choice(enemy_group.sprites())
                    enemy_bullet = EnemyBullet(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom)
                    bullet_group.add(enemy_bullet)
                    self.last_enemy_shot = time_now
                
                #only after the game 'starts'
                #we want to actually start updating the screen
                rocket_group.update()
                enemy_group.update()
                player_group.update()
                player_view.update()
                bullet_group.update()
            
            #timer to start game
            if self.countdown > 0:
                self.draw_text("GET READY", font2, green, int(width / 2 -150), int(height / 2 + 10))
                self.draw_text(str(self.countdown), font2, green, int(width / 2 -10), int(height / 2 + 70))
                count_timer = pygame.time.get_ticks()
                if count_timer - self.last_count > 1000:
                    self.countdown -= 1
                    self.last_count = count_timer

            #display updates
            pygame.display.update()
            pygame.display.flip()
         
#our player class
class PlayerState(pygame.sprite.Sprite):
    level = 1
    def __init__(self, player_x_pos, player_y_pos, playerchange, health) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('spaceship.png').convert_alpha()
        self.player_x_pos = player_x_pos
        self.player_y_pos = player_y_pos
        self.playerchange = playerchange
        self.rect = self.image.get_rect()
        self.rect.center = [self.player_x_pos, self.player_y_pos]
        self.last_shot = pygame.time.get_ticks()
        self.health = health
        self.health_left = health

    #our update player function
    def update(self):
        speed = 3
        game_over = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.rect.left < width - 110:
            player_view.rect.x += speed
        if key[pygame.K_LEFT] and self.rect.left > 0:
            player_view.rect.x -= speed

        self.mask = pygame.mask.from_surface(self.image)
        time_now = pygame.time.get_ticks()          
        if key[pygame.K_SPACE] and time_now - self.last_shot > cool_down:
            #plays sound effect when player shoots
            gun_fx.play()
            rocket = RocketState(self.rect.centerx, self.rect.top )
            rocket_group.add(rocket)
            self.last_shot = time_now

        pygame.draw.rect(screen, red, (self.rect.x , (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_left > 0:
            pygame.draw.rect(screen, green, (self.rect.x , (self.rect.bottom + 10), int(self.rect.width * (self.health_left / self.health)), 15))
        
        #when our health bar is gone to 0, we lose the game, display loss and score
        elif self.health_left<=0:
            self.kill()
            myGame.draw_text(self, "GAMER OVER!", font2, white, int(width / 2 -150), int(height / 2 + 10))
            myGame.draw_text(self, 'Score: {}'.format(RocketState.score), font1, red, int(width / 2 -10), int(height / 2 + 70))
            #delattr(self, self.health)
            game_over += 1
            

#create player object below
player_view = PlayerState(width/2, height - 130, 0, 3) 
player_group.add(player_view)

#player bullet/rocket
class RocketState(pygame.sprite.Sprite):
    score = 0
    def __init__(self, rocket_x_pos, rocket_y_pos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('rocket.png').convert_alpha()
        self.rocket_x_pos = rocket_x_pos
        self.rocket_y_pos = rocket_y_pos
        self.rect = self.image.get_rect()
        self.rect.center = [self.rocket_x_pos, self.rocket_y_pos]


    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            RocketState.score +=100

#enemy class    
class enemies(pygame.sprite.Sprite):
    move_down = 10
    def __init__(self, enemies_x, enemies_y):
        pygame.sprite.Sprite.__init__(self)
        self.enemies_x = enemies_x
        self.enemies_y = enemies_y
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [enemies_x, enemies_y]
        self.move_counter = 0
        self.move_direction = 1
        self.lose = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter +=1
        if abs(self.move_counter) > 100:
            self.move_direction *= -1 
            self.move_counter *= self.move_direction
            if self.move_counter < 100:
                self.rect.y += self.move_down
                
#enemy bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, bullet_x_pos, bullet_y_pos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.bullet_x_pos = bullet_x_pos
        self.bullet_y_pos = bullet_y_pos
        self.rect = self.image.get_rect()
        self.rect.center = [self.bullet_x_pos, self.bullet_y_pos]
    
    def update(self):
        self.rect.y += 3
        if self.rect.top < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()
            player_view.health_left -= 1
            RocketState.score -= 50

#main function
if __name__ == "__main__":
    my_game = myGame()
    my_game.run_game()

