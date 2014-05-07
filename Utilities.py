#Esteban Rojas and Danny McCormack
#CSE 30332 Final Project

import pygame
DIR = 'direction' # 'left', 'right', 'up', 'down'?
COORD = 'xy' #'x, y tuple'
ANGLE = 'angle' # 'degrees from 0'
FIRE = 'fired' # 'bool if fired projectile or not'
HEALTH = 'health' # 'current health to check death'
#Utilitiy function for rotating an image
def rot_center(image, angle):
    #rotate an image while keeping its center and size
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image