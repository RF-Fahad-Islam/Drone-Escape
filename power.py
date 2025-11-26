import pygame as pg

class PowerUp(pg.sprite.Sprite):
    def __init__(self,screen,x_pos,y_pos,scale_factor,type):
        super().__init__()
        if type == "speed":
            powerup_image = pg.image.load('assets/powerup.png').convert_alpha()
        elif type == "shield":
            powerup_image = pg.image.load('assets/powerup.png').convert_alpha()
        else:
            powerup_image = pg.image.load('assets/powerup.png').convert_alpha()
        self.image = pg.transform.scale_by(powerup_image, scale_factor)
        self.rect = self.image.get_rect(midtop=(x_pos,y_pos))
        self.type = type

    def update(self,dt,ground_speed):
        self.rect.x += int(ground_speed*dt)