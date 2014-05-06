#Esteban Rojas and Danny McCormack
#CSE 30332 Final Project

import pygame
import math
import sys
from player import Player
from projectile import Projectile



#Constants for getting data from network packet
from network import ANGLE
from network import COORD
from network import FIRE
from network import HEALTH  

# Class gamespace
class GameSpace:
	def main(self):
		# Basic init
		pygame.init()
		self.damage = 10
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		self.rect = pygame.Rect(0, 0, 640, 480)
		
		# Init game objects
		self.player1 = Player(self, 'player1.png', self, True)
		self.player2 = Player(self, 'player2.png', self, False)
		
		#Determine whether local player is player 1 or player 2
		localPlayer = sys.argv[1]
		
		localCoordinates = (200, 110)
		awayCoordinates = (200, 300)
		
		#Make the player start at the right place
		if localPlayer == "p1":
			self.player1.sprite_info[COORD] = localCoordinates
			self.player2.sprite_info[COORD] = awayCoordinates
		else:
			self.player1.sprite_info[COORD] = awayCoordinates
			self.player2.sprite_info[COORD] = localCoordinates		

		self.projectileList = []

	# Game single iteration loop
	def iteration(self, x, y, angle, fired, health):
		
		# update player2's data from network
		self.player2.sprite_info = self.assemble_data(x, y, angle, fired, health)

		# Handle firing from mouse click
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif pygame.mouse.get_pressed()[0]:
				self.player1.sprite_info[FIRE] = True
			elif not pygame.mouse.get_pressed()[0]:
				self.player1.sprite_info[FIRE] = False

		# Use WASD to move player, assign change in (x,y) accordingly
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_a] or keysPressed[pygame.K_d] or keysPressed[pygame.K_w] or keysPressed[pygame.K_s]:
			self.player1.move(keysPressed) 

		# update both players
		self.player1.update()
		self.player2.update()

		# update the projectiles
		for projectile in self.projectileList:
			projectile.tick()

		# update display
		self.display_game()


	def display_game(self):
		self.screen.fill(self.black)
		
		for projectile in self.projectileList:
			self.screen.blit(projectile.image, projectile.rect)
			
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)

		pygame.display.flip()

	# simple function to create matching dictionary from arguments
	# make loop iteration less cluttered
	def assemble_data(self, x, y, angle, fired, health):
		data = {
			COORD: (x, y),
			ANGLE: angle,
			FIRE: fired,
			HEALTH: health
		}
		return data


if __name__ == '__main__':
	# Declare gamespace
	gs = GameSpace()
	gs.main()
	
