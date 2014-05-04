# Main for pygame

import pygame
from player import Player 
from projectile import Projectile

# Class gamespace to 
class GameSpace:
	def main(self):
		# Basic init
		pygame.init()
		self.damage = 10
		self.size = self.width, self.height = 640,480
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		self.rect = pygame.Rect(0,0,640,480)

		# Init game objects
		self.player1 = Player(self, 'player1.png')
		self.player2 = Player(self, 'player2.png')

		self.proj_list = pygame.sprite.Group()

		# Game single iteration loop
	def while_iter(self):
		# From while pygame primer while loop

	def collision(self):
		# Track collisions




if __name__=='__main__':
	# Declare gamespace
	gs = GameSpace()
	gs.main()