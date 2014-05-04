import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, fname):
		# pass gamespace
		self.gs = gs
		# load image from argument
		self.image_name = "res/" + fname
		self.image = pygame.image.load(image_name).convert()
		self.rect = self.image.get_rect()
		self.angle = 0

		# original image to avoid resize errors
		self.orig_image = self.image
		self.frame = 0 # not sure if needed
		self.toFire = False

	# clock tick
	def tick(self):
		px = self.rect.centerx
		py = self.rect.centery
		# stop to fire
		if self.toFire = True:
			# create lazer
			pass

		else:
			# rotation
			self.mx, self.my = pygame.mouse.get_pos()
			center = self.rect.center
			self.angle = 225 - math.degrees(math.atan2(self.my-py, self.mx-px))
			self.image = pygame.transform.rotate(self.orig_image, self.angle)
			self.rect = self.image.get_rect()
			self.rect.center = center

	# update direction on mouse input, could be merged with tick
	def update(self, dir):
		self.speed = 5
		orig_rect = self.rect
		if self.tofire == True:
			return
		if dir == 'left':
			self.rect = self.rect.move(-self.speed, 0)
		if dir == 'right':
			self.rect = self.rect.move(self.speed, 0)
		if dir == 'down':
			self.rect = self.rect.move(0, self.speed)
		if dir == 'up':
			self.rect = self.rect.move(0, -self.speed)