import pygame
from pygame.locals import *
from sys import exit
import numpy
MARGIN_COEFFICIENT=2
screen_size=(800,600)
bg_color=(255,255,255)
font_color=(0,0,0)

# dot_image_file_path=f'./png/red_5_5.png'

pygame.init()
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("Poland: ")
screen.fill(bg_color)
# dot_image= pygame.image.load(dot_image_file_path).convert()

# 初始化时钟对象
clock = pygame.time.Clock()

# 初始化字体对象
font = pygame.font.Font(None, 20)

def coordinate_transform(R,coo,screen_size):
    r=min(screen_size)/2
    k=r/R
    return (coo[0]*k+screen_size[0]/2,-coo[1]*k+screen_size[1]/2)

# this draws an img at the pos of the dot, which is not used
# def draw(dot,R):
    # screen_r_vec = coordinate_transform(R, dot.r_vec, screen.get_size())
    # screen.blit(dot_image,screen_r_vec)
    
def step(unv):
    screen.fill(bg_color)
    clock.tick(300)
    
    fps=clock.get_fps()
    fps_text = font.render("FPS: {:.2f}".format(fps), True, font_color)
    Energy_correction_text=font.render("v *= : {:.2f}".format(unv.k_correct), True, font_color)
    Epcheck_text=font.render("Epcheck: {:.2f}".format(unv.Ep), True, font_color)
    screen.blit(fps_text, (40, 40))
    screen.blit(Energy_correction_text, (40, 60))
    screen.blit(Epcheck_text, (40, 80))
    dotj=unv.dotj
    R=unv.universe_R
    for dot in dotj:
        for neighboring_dot in dot.neighborj:
            t=min(int(abs(neighboring_dot.force)**2),255)
            if neighboring_dot.force>0:
                color=(t,0,(255-t)//2)
            else:
                color=(0,t,(255-t)//2)
            pygame.draw.line(
                screen,
                color,
                coordinate_transform(R,dot.r_vec,screen.get_size()),
                coordinate_transform(R,neighboring_dot.dot.r_vec,screen.get_size()),
                
                width=1,
            )
    pygame.display.flip()