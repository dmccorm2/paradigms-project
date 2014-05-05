import pygame
import network

# To-do:
# 	Booleon to determine if hosted player or other player?
# 	Set angle
# 	Save to data structure


class Player(pygame.sprite.Sprite):
	def __init__(self, fname):
		# pass gamespace
		self.gs = gs
		# load image from argument
		self.image_name = "res/" + fname
		self.image = pygame.image.load(image_name).convert()
		self.rect = self.image.get_rect()

		# values assigned in iteration loop loop function
		self.sprite_info = {
			COORD: (0,0), # CHANGE IN x,y (i.e. moves right, then x=speed, y=0)
			ANGLE: 0,
			FIRE: False,
			HEALTH: 100
		}
		# original image to avoid resize errors
		self.orig_image = self.image

	def update(self):
		orig_rect = self.rect
		self.rect = self.rect.move(self.sprite_info[COORD])

		if self.sprite_info[FIRE] == True:
			# create projectile
			# add to projectile list
			pass
		else:
			center = self.rect.center
			self.image = pygame.transform.rotate(self.orig_image, self.sprite_info[ANGLE])
			self.rect = self.image.get_rect()
			self.rect.center = center
			