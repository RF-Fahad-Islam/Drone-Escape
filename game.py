import pygame as pg
import os
import random
from sprites.drone import Drone
from sprites.pipe import Pipe
from sprites.power import PowerUp
from sprites.obstacle import Obstacle
import os 

pg.init()
pg.mixer.init()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) 
ASSETS = os.path.join(SCRIPT_DIR, 'assets')
flap_sound = pg.mixer.Sound(os.path.join(ASSETS, "sfx/flap.wav"))
point_sound = pg.mixer.Sound(os.path.join(ASSETS, "sfx/score.wav"))
powerup_sound = pg.mixer.Sound(os.path.join(ASSETS, "sfx/powerup.wav"))
dash_sound = pg.mixer.Sound(os.path.join(ASSETS, "sfx/dash.ogg"))
bgm = pg.mixer.Sound(os.path.join(ASSETS, "sfx/bgm.mp3"))
hit_sound = pg.mixer.Sound(os.path.join(ASSETS, "sfx/dead.wav"))
font_big = pg.font.Font(os.path.join(ASSETS,'font.ttf'), 50)
font_medium = pg.font.Font(os.path.join(ASSETS,'font.ttf'), 20)

class Game:
    def __init__(self):
        #MUSIC
        bgm.play(loops=-1)
        bgm.set_volume(0.3)
        # Initialize Screen
        self.width =600
        self.height = 950
        self.screen = pg.display.set_mode((self.width,self.height))
        self.scale_factor = 1.5
        self.clock = pg.time.Clock()
        self.fps =60
        self.is_started = False
        self.hiscore = 0
        self.is_sheilded = False
        self.shield_track = 0
        self.collision_skip = 0
        self.tracker =0
        self.dash_time = 2000
        # Game Constant Variables
        self.jump_speed = 600
        self.ground_speed= -300
        self.gravity = 100
        self.setupBgandGround()
        # Initialize Bird
        self.drone = Drone(self.screen, self.gravity, self.jump_speed, 0.1)
        self.is_flap = True
        self.drone_group = pg.sprite.GroupSingle()
        self.powers = pg.sprite.Group()
        self.obs = pg.sprite.Group()
        self.drone_group.add(self.drone)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.drone)
        # Initialize Pipes
        self.pipes = pg.sprite.Group()
        #Timer Events
        self.SPAWN_PIPE = pg.USEREVENT + 1
        self.SPAWN_PIPE_TIMER = 1400
        self.SPAWN_POWER = pg.USEREVENT + 2 
        self.SPAWN_OBS = pg.USEREVENT + 3
        pg.time.set_timer(self.SPAWN_POWER, random.randint(2000,7000))
        pg.time.set_timer(self.SPAWN_PIPE, self.SPAWN_PIPE_TIMER) 
        pg.time.set_timer(self.SPAWN_OBS, random.randint(2000,7000)) 
        self.game_initial_values()
    
    def welcome_screen(self):
        
        # Game title
        title = font_big.render("Drone Escape", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.width//2, self.height//3))
        self.screen.blit(title, title_rect)
        
        # Instruction
        instr = font_medium.render("Triple SPACE to Start", True, (255, 255, 255))
        instr_rect = instr.get_rect(center=(self.width//2, self.height//2.5))
        self.screen.blit(instr, instr_rect)
        instr2 = font_medium.render("Press X to Dash", True, (255, 255, 255))
        instr2_rect = instr2.get_rect(center=(self.width//2, self.height//2.2))
        self.screen.blit(instr2, instr2_rect)
        
        pg.display.update()

    
    def game_initial_values(self):
        #To start new game and initialize values
        self.drone.rect = self.drone.image.get_rect(center=(self.screen.get_width()/10, self.screen.get_height()/2))
        self.drone.velocity_y = 0
        self.pipes.empty()
        self.pipe_gap = 200
        self.game_over = False
        self.min_pipe_gap = 120
        self.is_flap = True
        self.is_started = False
        self.score = 0
        self.score_manager()
    
    def setupBgandGround(self):
        # Initialize Background
        bg_img_load = pg.image.load(os.path.join(ASSETS,'bg.png')).convert()
        self.bg_img = pg.transform.scale(bg_img_load, (600,950))
        self.running = True
        # Initialize Ground
        self.ground_img1 = pg.transform.scale(pg.image.load(os.path.join(ASSETS,'ground.png')).convert_alpha(),(600,250))
        self.ground_img2 = pg.transform.scale(pg.image.load(os.path.join(ASSETS,'ground.png')).convert_alpha(),(600,250))
        self.shield_img = pg.transform.scale(pg.image.load(os.path.join(ASSETS,'powerup_shield.png')).convert_alpha(),(50,50))
        self.ground_rect = self.ground_img1.get_rect()
        self.ground_rect2 = self.ground_img2.get_rect()
        self.ground_rect.x = 0
        self.ground_rect.y, self.ground_rect2.y = 740,740
    
    def game_over_screen(self, score):
        self.screen.fill((0, 0, 0))
        bgm.stop()
        # Main "GAME OVER" title
        text1 = font_big.render("GAME OVER", True, (255, 50, 50))
        rect1 = text1.get_rect(center=(self.screen.get_width()//2, 200))
        self.screen.blit(text1, rect1)
        self.score = int(self.score)
        # Score text
        text2 = font_medium.render(f"Score: {score}", True, (255, 255, 255))
        rect2 = text2.get_rect(center=(self.screen.get_width()//2, 280))
        self.screen.blit(text2, rect2)
        # High score text
        text3 = font_medium.render(f"High Score: {self.hiscore}", True, (255, 255, 255))
        rect3 = text3.get_rect(center=(self.screen.get_width()//2, 320))
        self.screen.blit(text3, rect3)

        # Restart instruction
        text4 = font_medium.render("Press SPACE to Restart", True, (180, 180, 180))
        rect4 = text4.get_rect(center=(self.screen.get_width()//2, 350))
        self.screen.blit(text4, rect4)
        
        self.score_manager(score=int(score))

    def score_manager(self, score=None):
        self.hiscore = 0
        if not os.path.exists('hiscore.txt'):
            with open('hiscore.txt','w') as f:
                f.write('0')
        with open('hiscore.txt','r+') as f:
            try:
                self.hiscore= int(f.read())
            except:
                pass
        if score is None:
            return self.hiscore
        
        else:
            with open("hiscore.txt",'r+') as f:
                try:
                    self.hiscore = int(f.read())
                except:
                    self.hiscore = 0
                if score > self.hiscore:
                    f.write(str(score))
    
    def count_score(self):
        # Score text
        for pipe in self.pipes:
            if pipe.rect.left+5 < self.drone.rect.right and not self.game_over and not pipe.scored:
                self.score += 0.5  # Increment score by 0.5 for each pipe passed
                pipe.scored = True
                self.SPAWN_PIPE_TIMER-=50
                self.SPAWN_PIPE_TIMER = max(900,self.SPAWN_PIPE_TIMER)
                pg.time.set_timer(self.SPAWN_PIPE, self.SPAWN_PIPE_TIMER) 
                point_sound.play()

    
    def start(self):
        # Start Game Loop
        pg.display.set_caption("Drone Escape - By Fahad")
        self.gameloop()
    
    def run_ground(self,dt):
            self.ground_rect.x += int(self.ground_speed*dt)
            self.ground_rect2.x = self.ground_rect.right
            if abs(self.ground_rect.left) > self.screen.get_width():
                self.ground_rect.x = 0

    def reset(self):
        self.game_initial_values()
        pg.display.update()
        
    
    def drawAll(self):
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.ground_img1,self.ground_rect)
        self.screen.blit(self.ground_img2,self.ground_rect2)
        sc = font_big.render(f"{int(self.score)}", True, (255, 255, 255))
        rect2 = sc.get_rect(topright=(self.width-10,40))
        sh =font_medium.render(f"Hi: {self.hiscore}", True, (255, 255, 255))
        rect3 = sh.get_rect(topleft=(10,10))
        s = font_big.render(f"{'()' if self.is_sheilded else ''}", True, (255, 255, 255))
        rect1 = s.get_rect(center=(self.width//2,50))
        self.screen.blit(s, rect1)
        self.screen.blit(sh, rect3)
        self.screen.blit(sc, rect2)
        # t = font_medium.render(f")x{self.collision_skip}", True, (255, 255, 255))
        # self.screen.blit(t,(self.width-50,10))
        
    def updateEverything(self,dt):
         # Update Sprites
        for pipe in self.pipes:
            pipe.update(dt,self.ground_speed)
            if pipe.rect.right < 0:
                pipe.kill()
                self.all_sprites.remove(pipe)
                
        #Update PowerUps
        for power in self.powers:
            power.update(dt,self.ground_speed)
            if power.rect.right < 0:
                power.kill()
                self.all_sprites.remove(power)
                
        #Update Obstacles
        for ob in self.obs:
            ob.update(dt,self.ground_speed*2)
            if ob.rect.right < 0:
                ob.kill()
                self.all_sprites.remove(ob)
        
    def handleCollisions(self):
        if pg.sprite.spritecollide(self.drone_group.sprite, self.pipes, False) and not self.is_sheilded:
            self.gravity = 0
            self.ground_speed = 0
            self.is_flap = False
            self.game_over = True
            
        hits = pg.sprite.spritecollide(self.drone_group.sprite, self.powers, True) 
        if hits:
            for power in hits:
                if power.type == "speed":
                    self.score += 5  # Increase score by 5 for collecting power-up
                elif power.type == "shield":
                        self.is_sheilded = True
                        self.shield_track = 0
            
            powerup_sound.play()

        if pg.sprite.spritecollide(self.drone_group.sprite, self.obs, False):
            if self.collision_skip>0:
                self.collision_skip -= 1
                return
            self.gravity = 0
            self.ground_speed = 0
            self.is_flap = False
            self.game_over = True
            self.collision_skip = 0
            hit_sound.play()
        
        if (self.drone.rect.bottom >= 740 or self.drone.rect.top <= 0) and not self.game_over:
            if self.collision_skip>0:
                self.collision_skip -= 1
                return
            self.game_over = True
            self.collision_skip = 0
            hit_sound.play()
    
    def gameloop(self):
        while self.running:
            self.screen.blit(self.bg_img,(0,0))
            dt = self.clock.get_time()/1000
            keys = pg.key.get_pressed()
            
            if self.is_sheilded:
                self.shield_track += 1
                if self.shield_track > 300:
                    self.is_sheilded = False
                    self.shield_track = 0
            
            if not self.is_started:
                self.gravity = 0
                self.welcome_screen()
                if keys[pg.K_SPACE]:
                    self.is_started = True
            else:
                self.gravity = 100
            # !Event Handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    quit()
                    
                # Spawn Pipes
                if event.type == self.SPAWN_PIPE and not self.game_over:
                    self.pipe_height = random.randint(200, 600)
                    self.pipe = Pipe(self.screen, self.width+50, self.pipe_height, self.scale_factor, False)
                    self.pipe_flipped = Pipe(self.screen, self.width+50, self.pipe.rect.y - self.pipe_gap-self.pipe.rect.height, self.scale_factor, True)
                    self.pipes.add(self.pipe)
                    self.pipes.add(self.pipe_flipped)
                    # add the two pipe sprites directly to the all_sprites group
                    self.all_sprites.add(self.pipe, self.pipe_flipped)
                    self.pipe_gap-=5
                    self.pipe_gap = max(self.min_pipe_gap,self.pipe_gap)
                    self.ground_speed -= 10
                    
                
                #Power Up
                if event.type == self.SPAWN_POWER and not self.game_over:
                    self.power = PowerUp(self.screen, random.randint(self.width+50,self.width+300), random.randint(100,500), 0.25, random.choice(["speed","shield"]))
                    self.all_sprites.add(self.power)
                    self.powers.add(self.power)
                
                #Obstacle
                if event.type == self.SPAWN_OBS and not self.game_over:
                    self.ob = Obstacle(self.screen, random .randint(self.width+50,self.width+300),random.randint(50,600), 0.1)
                    self.all_sprites.add(self.ob)
                    self.obs.add(self.ob)
                
                if event.type == pg.KEYDOWN and (event.key == pg.K_SPACE or keys[pg.K_UP]) and not self.game_over and self.is_flap:
                    flap_sound.play()
                    self.drone.flap(dt)
                
                #Dash
                if event.type == pg.KEYDOWN and event.key == (pg.K_RIGHT or event.key == pg.K_x) and not self.game_over and self.tracker>150:
                    dash_sound.play()
                    self.ground_speed = -1000
                else:
                    self.ground_speed = -300
                    
            self.tracker+=1
                    
                    
            if self.game_over and self.is_started:
                pg.time.set_timer(self.SPAWN_PIPE, 0)
                self.game_over_screen(score=self.score)
                pg.display.update()
                keys = pg.key.get_pressed()
                #New Game on Space Press
                if keys[pg.K_SPACE]:
                    self.running = False
                    Game().start()
                    
            elif not self.game_over and self.is_started:
                
                self.updateEverything(dt)
                
                self.handleCollisions()
                

                        
                self.run_ground(dt)
                self.drone.run(dt)
                self.drawAll() 
                self.count_score()
                pg.display.update()
                self.clock.tick(self.fps)
            
game = Game()
game.start()