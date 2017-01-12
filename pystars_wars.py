
# Importamos las librerias necesarias
import random, os, pygame
import animation
import level
import gutils, ships, constants
from pygame.locals import *


MAX_Y_TILES = 30
MAX_X_TILES = 23


class BackTile(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)



class Background:
	def __init__(self, layout):
		self.images = []
		for i in range(0, 14):
			self.images.append(gutils.load_image("backtile_" + str(i) + ".png", i == 0)[0])
	
		self.layout = layout

		self.backtiles = []
		for j in range(0,MAX_Y_TILES):
			tiles = []
			for i in range(0,MAX_X_TILES):
				tiles.append(BackTile())
			self.backtiles.append(tiles)

		for j in range(0,MAX_Y_TILES):
			for i in range(0,MAX_X_TILES):
				a = int(self.layout[j][i])
				image = self.images[a]
				self.backtiles[j][i].image = image

		self.resetBackTiles()

		self.counter = 0
		self.steps = 0
		self.line_counter = len(self.layout) - MAX_Y_TILES
		
		self.group = pygame.sprite.RenderClear()
		for j in range(0,MAX_Y_TILES):
			for i in range(0,MAX_X_TILES):
				self.group.add(self.backtiles[j][i])

	def draw(self, surface):
		self.group.draw( surface )

	def clear(self, screen, background):
		self.group.clear(screen , background)
		
	def resetBackTiles(self):
		for j in range(0,MAX_Y_TILES):
			for i in range(0,MAX_X_TILES):
				self.backtiles[j][i].rect =  pygame.Rect(i * 32, j * 32  - 32, 32, 32)

	def updateBackTiles(self):
		for j in range(0,MAX_Y_TILES):
			for i in range(0,MAX_X_TILES):
				self.backtiles[j][i].rect.move_ip(0, 1)

	def update(self):
		self.updateBackTiles()
		self.steps += 1

		if self.steps % 32 == 0:
			row = self.backtiles[-1:]
			self.backtiles.pop()
			self.backtiles.insert(0, row[0])

			for i in range(0,MAX_X_TILES):
				a = int(self.layout[self.line_counter][i])
				row[0][i].image = self.images[a]

			self.resetBackTiles()

			self.line_counter += 1
			if self.line_counter == len(self.layout) - 1 : self.line_counter = 0

def draw_text(screen, text, line):
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render(text , 1, (255, 0, 0))
		textpos = text.get_rect(centerx = 50, centery = line * 30)
		textpos.left = 0
		screen.blit(text, textpos)


def add_enemies(group):
	a = random.randint(0, 500)
	if a < 10:
		group.add(ships.EnemyRing(random.randint(32, constants.SCREEN_WIDTH)))

aengine = None

def main():


	score = 0
	lost_ships = 0

	level1 = level.Level('level1.lvl')

	random.seed()
	pygame.init()
	screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), HWSURFACE|DOUBLEBUF)

	animation.init_animations()

	pygame.display.set_caption( "Primer ejemplo" )

	background_image, background_rect = gutils.load_image("background.bmp")
	screen.blit(background_image, (0,0))

	shipSprite = pygame.sprite.RenderClear()
	ship = ships.Nave((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT - 1))
	shipSprite.add(ship)

	enemies = pygame.sprite.RenderClear()
	enemy = ships.Enemy()
	enemies.add(enemy)


	lasers = pygame.sprite.RenderClear()

	running = True
	clock = pygame.time.Clock()

	back = Background(level1.layout)

	explosions = pygame.sprite.RenderClear()
	enemy_shoots = pygame.sprite.RenderClear()

	bomb = gutils.load_SoundFile("bomb.wav")
	ship_explotion = gutils.load_SoundFile("ship_explotion.wav")
	caching = gutils.load_SoundFile("chaching.wav")

	pause = False
	while running is True:
		clock.tick(60) 

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False # Se acaba el juego
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False # Se acaba el juego
				elif event.key == K_p:
					pause = not pause # Se acaba el juego
				else:
					ship.proccessKey(event, lasers)	
			elif event.type == KEYUP:
				ship.proccessKey(event, lasers)	


		shipSprite.clear( screen, background_image )
		lasers.clear( screen, background_image )
		enemies.clear( screen, background_image )
		back.clear( screen, background_image )
		explosions.clear( screen, background_image )
		enemy_shoots.clear( screen, background_image )

		if not pause:
			add_enemies(enemies)
			back.update()
			shipSprite.update()
			enemies.update()
			lasers.update()
			explosions.update()
			enemy_shoots.update()

		for hit in pygame.sprite.groupcollide( enemies, lasers, 1, 1):
			explosions.add(animation.Explotion(hit.rect.center))
			bomb.play()
			score += 1
			if score % 10 == 0: caching.play()

		for hit in pygame.sprite.groupcollide( shipSprite, enemy_shoots, 1, 1):
			explosions.add(animation.Explotion(hit.rect.center))
			ship = ships.Nave((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT - 1))
			shipSprite.add(ship)
			ship_explotion.play()
			lost_ships += 1

		for hit in pygame.sprite.groupcollide( shipSprite, enemies, 1, 0):
			explosions.add(animation.Explotion(hit.rect.center))
			ship = ships.Nave((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT - 1))
			shipSprite.add(ship)
			ship_explotion.play()
			lost_ships += 1


		back.draw(screen)
		shipSprite.draw( screen )
		enemies.draw( screen )
		lasers.draw(screen)
		explosions.draw(screen)
		enemy_shoots.draw(screen)

		draw_text(screen, 'Score %d' % score, 1)
		draw_text(screen, 'Bombas %d' % ship.get_weapon_bullets(), 2)
		draw_text(screen, 'Muertes %d' % lost_ships, 3)

		for enemy in enemies : enemy.do_shoot(enemy_shoots)

		pygame.display.flip()
        
	raise SystemExit

if __name__ == '__main__': main()
