import pygame as pg

class Drone(pg.sprite.Sprite):
    def __init__(self,screen,gravity,jump_speed,scale_factor):
        drone_img1 = pg.image.load('assets/dronedown.png').convert_alpha()
        drone_img2 = pg.image.load('assets/droneup.png').convert_alpha()
        super().__init__()
        # Initialize drone properties
        self.gravity = gravity
        self.velocity_y = 0
        self.scale_factor = scale_factor
        self.jump_speed = jump_speed
        self.img_list = [pg.transform.scale_by(drone_img1, self.scale_factor),pg.transform.scale_by(drone_img2, self.scale_factor)]
        self.img_init = 0
        self.image = self.img_list[self.img_init]
        self.rect = self.image.get_rect(center=(screen.get_width()/10, screen.get_height()/2))
        self.anim_cnt = 1
    
    def playAnimation(self):
        self.anim_cnt += 1
        if self.anim_cnt > 8:
            self.anim_cnt = 1
            self.img_init = 0 if self.img_init == 1 else 1
            self.image = self.img_list[self.img_init]
        
    def run(self,dt):
        # drone Animation
        self.playAnimation() 
            
        # drone Movement
        self.apply_gravity(dt)
        if self.rect.bottom >= 750:
            self.rect.y = 750 - self.rect.height
        if self.rect.top <= 0:
            self.rect.y = 0
        
    def apply_gravity(self,dt):
        self.velocity_y += int(self.gravity * dt)
        self.rect.y += self.velocity_y
        
    def flap(self,dt):
        self.velocity_y = -int(self.jump_speed * dt)
        self.image = pg.transform.rotate(self.image,25)
        self.img_init = 1
        self.image = self.img_list[self.img_init]