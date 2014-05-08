#Esteban Rojas and Danny McCormack
#CSE 30332 Final Project

import pygame
import math
import Utilities

# To-do:
# 	Save to data structure

from projectile import Projectile

from Utilities import ANGLE
from Utilities import COORD
from Utilities import FIRE
from Utilities import HEALTH

SPEED = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, fname, isLocal, gs = None):
        # pass gamespace
        self.gs = gs
        # load image from argument
        print str(fname)
        self.image_name = "res/" + str(fname)
        self.image = pygame.image.load(self.image_name).convert()
        self.rect = self.image.get_rect()
        self.explosionCounter = 0
        #Used to determine if this player is the local or networked player
        self.isLocal = isLocal

        # values assigned in iteration loop loop function
        self.sprite_info = {
			COORD: (0, 0), # CHANGE IN x,y (i.e. moves right, then x=speed, y=0)
			ANGLE: 0,
			FIRE: False,
			HEALTH: 1000
		}
        
        # original image to avoid resize errors
        self.orig_image = self.image
        self.explosionImages = []
        # load the explosion images for when the player explodes
        for i in range(0, 17):
            filename = ""
            if i < 10:
                filename = "res/explosion/frames00" + str(i) + "a.png"
            else:
                filename = "res/explosion/frames0" + str(i) + "a.png"
            self.explosionImages.append(pygame.image.load(filename).convert())


    def move(self, eventList):
        if eventList[pygame.K_a]:
            self.sprite_info[COORD] = (-SPEED, 0)
        elif eventList[pygame.K_d]:
            self.sprite_info[COORD] = (SPEED, 0)
        elif eventList[pygame.K_w]:
            self.sprite_info[COORD] = (0, -SPEED)
        elif eventList[pygame.K_s]:
            self.sprite_info[COORD] = (0, SPEED)
            
        self.rect = self.rect.move(self.sprite_info[COORD])
        
        #FIXME: Send the data to the network

    #Update the current player's variables
    def update(self):
        #Update the right set of images and variables depending on whether the player is still alive
        
        if self.sprite_info[HEALTH] >= 0:
            self.ship_update()
        else:
            self.explosion_update()
            
    #The update function used if the player has not exploded yet
    def ship_update(self):
        
        #Calculate rotation, only if local player
        if self.isLocal:
            self.sprite_info[ANGLE] = self.calculate_angle()
        # if not self.isLocal:
        #     self.rect = self.rect.move(self.sprite_info[COORD])
        
        #orig_rect = self.rect
        #self.rect = self.rect.move(self.sprite_info[COORD])
                
        if self.sprite_info[FIRE] == True:
            rotationRad = math.radians(self.sprite_info[ANGLE])
            
            # create projectile with the correct velocities to match the player's angle
            speedMultiplier = 5
            projectileRad = rotationRad - math.pi / 2
            xspeed = -(math.cos(projectileRad) * speedMultiplier + (math.pi / 2))
            yspeed = math.sin(projectileRad) * speedMultiplier + (math.pi / 2)
            
            newProjectile = Projectile(self.gs, self.rect.centerx, self.rect.centery, xspeed, yspeed)
            
            # add to projectile list
            self.gs.projectileList.append(newProjectile)
            
        #Update the image based on the mouse position
        self.image = Utilities.rot_center(self.orig_image, self.sprite_info[ANGLE] + 40)
        
        #Check if the player's ship is colliding with a projectile
        hasCollision = False
        
        for projectile in self.gs.projectileList:
            if self.rect.colliderect( projectile.rect):
                hasCollision = True
                break
        
        #Update the life points, and change the player into an explosion if necessary
        if hasCollision:
            #A collision occurred            
            self.sprite_info[HEALTH] = self.sprite_info[HEALTH] - 100
            
            #Check if the health has been depleted
            if self.sprite_info[HEALTH] <= 0:
                self.explosionCounter = pygame.time.get_ticks()
                self.image = self.explosionImages[0]
                pygame.mixer.music.load("res/explode.wav")
                pygame.mixer.music.play()
        
    
    #The update function used if the player has exploded,
    # or is in the process of exploding
    def explosion_update(self):
        #process the other ticks of the explosion
        currTick = pygame.time.get_ticks()
        index = ((currTick - self.explosionCounter) / 10) / 16
        if index <= 16:
            self.image =self.explosionImages[index]
        else:
            self.image = pygame.image.load("res/empty.png").convert()

    # function to calculate rotation angle from mouse direction
    def calculate_angle(self):
        mx, my = pygame.mouse.get_pos()
        px, py = self.rect.center

        rotationRad = math.atan2(px, py)
        
        #TODO: Might need to add a constant to this
        rotationDeg = math.degrees(rotationRad) 

        return rotationDeg
