# Main for pygame

import pygame
from player import Player 
from projectile import Projectile
SPEED = 5
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
		key=pygame.key.get_pressed()
		if key[pygame.K_a]:self.player1.sprite_info[COORD] = (-SPEED, 0)
		if key[pygame.K_d]:self.player1.sprite_info[COORD] = (SPEED, 0)
		if key[pygame.K_w]:self.player1.sprite_info[COORD] = (0, -SPEED)
		if key[pygame.K_s]:self.player1.sprite_info[COORD] = (0, SPEED)

		# assign calculated rotation angle for local player
		self.player1.sprite_info[ANGLE] = calculate_angle(self)

		# update both players
		self.player1.update()
		self.player2.update()

		# update display
		self.display_game()


	def display_game(self):
		self.screen.fill(self.black)
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)
		pygame.display.flip()

	# function to calculate rotation angle from mouse direction
	def calculate_angle(self):
		mx, my = pygame.mouse.get_pos()
		px, py = self.rect.center
		angle = 315 - math.degrees(math.atan2(my-py, mx-px))
		return angle

	# simple function to create matching dictionary from arguments
	# make loop iteration less cluttered
	def assemble_data(self, x, y, angle, fired, health):
		data = {
			COORD: (x,y),
			ANGLE: angle,
			FIRE: fired
			HEALTH: health
		}
		return data



if __name__=='__main__':
	# Declare gamespace
	gs = GameSpace()
	gs.main()