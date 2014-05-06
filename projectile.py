#Esteban Rojas and Danny McCormack
#CSE 30332 Final Project

import pygame
import Utilities

class Projectile(pygame.sprite.Sprite):
    def __init__(self, gs = None, initX = 0, initY = 0, hspeed = 10, vspeed = 0, angle = 0):
        pygame.sprite.Sprite.__init__(self)
        
        self.gs = gs
        self.image = pygame.image.load("res/projectile.png").convert()
        self.rect = self.image.get_rect()
        
        self.hspeed = hspeed
        self.vspeed = vspeed
        
        #Tilt the image
        self.image = Utilities.rot_center(self.image, angle)
        
        #Make it start at the local player's position
        self.rect.centerx = initX
        self.rect.centery = initY
        
        #keep original image to limit resize errors
        self.orig_image = self.image
    
    def tick(self):
        #Update the position of the projectile on the screen
        self.rect = self.rect.move(self.hspeed, self.vspeed)