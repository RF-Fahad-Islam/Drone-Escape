import pygame as pg

class Pipe(pg.sprite.Sprite):
    def __init__(self,screen,x_pos,y_pos,scale_factor,is_flipped):
        super().__init__()
        pipe_image = pg.image.load('assets/pipeup.png').convert_alpha()
        self.image = pg.transform.scale_by(pipe_image, scale_factor)
        self.rect = self.image.get_rect(midtop=(x_pos,y_pos))
        self.scored = False
        if is_flipped:
            self.image = pg.transform.flip(self.image, False, True)

    def update(self,dt,ground_speed):
        self.rect.x += int(ground_speed*dt)