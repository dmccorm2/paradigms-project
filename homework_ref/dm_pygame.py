# Dan McCormack
# 4/16/14
# Paradigms
# PyGame Primer



import pygame
import math
import numpy

class Player(pygame.sprite.Sprite) 	:
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("deathstar.png").convert()
		self.image = pygame.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect()
		self.hit_box = pygame.Rect(0, 0, .95*self.rect.width, .95*self.rect.height)
		self.angle = 0
		# keep original image to limit resize errors

		self.orig_image = self.image
		self.frame = 0
		#fire flag
		self.tofire = False

	def tick(self):
		#get mouse pos		

		px = self.rect.centerx
		py = self.rect.centery
		#print str(mx) + " " + str(my) + "\n" + str(px) + " " + str(py) + "\n\n"
		#don't move while fiiring
		if self.gs.enemy.explode:
			self.gs.enemy.rect = pygame.Rect(0, 250, 400, 400)
			if self.frame < 17:
				iname = "explosion/frames" + "{0:03d}".format(self.frame) + "a.png"
				self.frame += 1
				self.gs.enemy.image = pygame.image.load(iname)
			else:
				self.gs.enemy.image = pygame.image.load("empty.png").convert()
				self.gs.enemy.rect = pygame.Rect(0, 0, 0, 0)
		if self.tofire == True:
			laser = Laser(self)
			self.gs.laser_list.add(laser)
		else:
			self.mx, self.my = pygame.mouse.get_pos()
			center = self.rect.center
			self.angle = 225 - math.degrees(math.atan2(self.my-py, self.mx-px))
		#	print str(self.angle)
			self.image = pygame.transform.rotate(self.orig_image, self.angle)
			self.rect = self.image.get_rect()
			self.rect.center = center


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
		self.hit_box.center = self.rect.center
		if self.gs.collision(self) or not self.gs.rect.contains(self.hit_box):
			self.rect = orig_rect

		

class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		
		self.image = pygame.image.load("globe.png").convert()
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(-100, 250)
		self.hit_box = pygame.Rect(-100, 250, 390, 390)
		self.explode_sound = pygame.mixer.Sound("explode.wav")

		self.orig_image = self.image
		self.health = 1000
		self.explode = False

	def hit(self):
		self.health -= self.gs.damage
		if self.health <= 100:
			self.image = pygame.image.load("globe_red100.png").convert()
		if self.health == 0:
			self.explode_sound.play(0)
			self.explode = True
			

class Laser(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("laser.png").convert()
		self.rect = self.image.get_rect()
		self.speed = 10
		self.angle = self.gs.angle
		self.rect.center = self.gs.rect.center
		self.vector = numpy.array([self.gs.mx - self.gs.rect.centerx, self.gs.my - self.gs.rect.centery])
		self.dir = numpy.linalg.norm(self.vector)

	def update(self):
		self.rect = self.rect.move(self.speed*self.vector[0]/self.dir, self.speed*self.vector[1]/self.dir)


class GameSpace:
	def main(self):
		# 1) Basic Init
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.set_num_channels(1)
		self.damage = 10
		self.size = self.width , self.height = 640,480
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		self.rect = pygame.Rect(-1, 1, 650, 490)
		# 2) init game objects
		self.clock = pygame.time.Clock()
		self.player = Player(self)
		self.enemy = Enemy(self)
		self.laser_list = pygame.sprite.Group()
		self.laser_sound = pygame.mixer.Sound("screammachine.wav")
		# 3) start game loop
		while 1:
			# 4) FPS
			self.clock.tick(60)

			# 5) user input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				elif pygame.mouse.get_pressed()[0]:
					self.player.tofire = True
					#pygame.mixer.music.load("screammachine.wav")
					self.laser_sound.play(0)
				elif not pygame.mouse.get_pressed()[0]:
					self.player.tofire = False
					self.laser_sound.stop()
			key=pygame.key.get_pressed()
			if key[pygame.K_a]:self.player.update('left')
			if key[pygame.K_d]:self.player.update('right')
			if key[pygame.K_w]:self.player.update('up')
			if key[pygame.K_s]:self.player.update('down')
			for laser in self.laser_list:
				if not self.rect.contains(laser.rect):
					self.laser_list.remove(laser)
				if self.collision(laser):
					self.enemy.hit()
					self.laser_list.remove(laser)
			# 6) send to tick to all objects
			self.player.tick()
			self.laser_list.update()
			# 7) display game objcets
			self.screen.fill(self.black)
			self.laser_list.draw(self.screen)
			self.screen.blit(self.enemy.image, self.enemy.rect)
			self.screen.blit(self.player.image, self.player.rect)
			pygame.display.flip()


	def collision(self, sprite):
		lx = sprite.rect.centerx
		ly = sprite.rect.centery
		ex = self.enemy.rect.centerx
		ey = self.enemy.rect.centery
		x = ex - lx
		y = ey - ly
		vector =numpy.array([x, y])
		er = 175
		lr = sprite.image.get_height() / 2
		if numpy.linalg.norm(vector) <= er + lr:
			return True
		else:
			return False

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()