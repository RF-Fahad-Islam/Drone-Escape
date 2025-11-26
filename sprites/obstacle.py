import pygame as pg

class Obstacle(pg.sprite.Sprite):
    def __init__(self,screen,x_pos,y_pos,scale_factor):
        super().__init__()
        obstacle_image = pg.image.load('assets/obstacle.png').convert_alpha()
        self.image = pg.transform.scale_by(obstacle_image, scale_factor)
        self.rect = self.image.get_rect(midtop=(x_pos,y_pos))
        self.image = pg.transform.rotate(self.image, angle=180)
        self.image = pg.transform.flip(self.image, True, False)

    def update(self,dt,ground_speed):
        self.rect.x += int(ground_speed*dt)