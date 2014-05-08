#Esteban Rojas and Danny McCormack
#CSE 30332 Final Project
# 5/7/14

import pygame
import math
import sys
from player import Player
from projectile import Projectile
import cPickle as pickle # for performance to help syncing across network
import pprint


#Constants for getting data from network packet
from Utilities import ANGLE
from Utilities import COORD
from Utilities import FIRE
from Utilities import HEALTH


# Class gamespace
class GameSpace:
	def main(self, localPlayer, send_func):
		# Basic init
		pygame.init()
		self.send_func = send_func
		self.damage = 10
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		self.rect = pygame.Rect(0, 0, 640, 480)
		
		# Init game objects
		self.player1 = Player('player1.png', True, self)
		self.player2 = Player('player2.png', False, self)
		
		#Determine whether local player is player 1 or player 2
		
		localCoordinates = (200, 110)
		awayCoordinates = (200, 300)
		
		#Make the player start at the right place
		if localPlayer == "p1":
			self.player1.rect.center = localCoordinates
			self.player2.rect.center = awayCoordinates
		else:
			self.player1.rect.center = awayCoordinates
			self.player2.rect.center = localCoordinates		

		self.projectileList = []

	# Game single iteration loop
	# Get data (pickled from network)
	def get_remote(self, data):
		# use try and catch to only receive pickled information
		try:
			self.player2.sprite_info = pickle.loads(data)
			pprint.pprint(self.player2.sprite_info)
			#self.player2.rect = self.player2.rect.move(self.player2.sprite_info[COORD])
		except Exception, e:
			print e

		
	def iteration(self):
		# update player2's data from network
		# Handle firing from mouse click
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif pygame.mouse.get_pressed()[0]:
				self.player1.sprite_info[FIRE] = True
				#self.send_func(pickle.dumps(self.player1.sprite_info))
			elif not pygame.mouse.get_pressed()[0]:
				self.player1.sprite_info[FIRE] = False

		# Use WASD to move player, assign change in (x,y) accordingly
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_a] or keysPressed[pygame.K_d] or keysPressed[pygame.K_w] or keysPressed[pygame.K_s]:
			self.player1.move(keysPressed) 
			self.send_func(pickle.dumps(self.player1.sprite_info))

		# update both players
		self.player1.update()
		self.player2.update()
		self.send_func(pickle.dumps(self.player1.sprite_info))

		# update the projectiles
		for projectile in self.projectileList:
			projectile.tick()

		# update display
		self.display_game()

	# basic function to handle blitting, etc.
	def display_game(self):
		self.screen.fill(self.black)
		
		for projectile in self.projectileList:
			self.screen.blit(projectile.image, projectile.rect)
			
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)

		pygame.display.flip()


