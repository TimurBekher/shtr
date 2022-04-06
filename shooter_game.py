#Создай собственный Шутер!

from pygame import *
from random import randint
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("SHOOTER")
background = image.load('galaxy.jpg')
background = transform.scale(background, (win_width, win_height))
FPS = 250
#Загружаем музыку
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
#################
kills = 0 #убитые враги
lost = 0#пропущенные
######Надписи########
font.init()
font14=font.SysFont('Arial',14)
text_killed = font14.render("Убито:"+str(kills),True,(255,0,0))
text_lost = font14.render("Пропущено:"+str(lost),True,(255,0,0))
font24=font.SysFont('Arial',24)
text_win = font24.render("ПОБЕДА!",True,(255,0,0))
text_lost = font24.render("ПРОИГРЫШ!",True,(255,0,0))

######################################
class GameSprite(sprite.Sprite):
	def __init__(self,img,w,h,x,y,speed):
		sprite.Sprite.__init__(self)
		self.w=w 
		self.h=h 
		self.image = image.load(img)
		self.image = transform.scale(self.image, (self.w, self.h))
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.speed=speed
	def reset(self):
		window.blit(self.image ,(self.rect.x, self.rect.y))
######################################
class Player(GameSprite):
	def __init__(self,img,w,h,x,y,speed):
		GameSprite.__init__(self,img,w,h,x,y,speed)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.w<win_width:
			self.rect.x+=self.speed
	def fire(self):
		bullet = Bullet(img="bullet.png",w=20,h=20,x=self.rect.x,y=self.rect.y,speed=1)
		bullets.add(bullet)
######################################
class UFO(GameSprite):
	def __init__(self,img,w,h,x,y,speed):
		GameSprite.__init__(self,img,w,h,x,y,speed)
	def update(self):
		global lost,text_lost
		self.rect.y+= self.speed
		if self.rect.y>win_height:
			lost+=1
			text_lost = font14.render("Пропущено:"+str(lost),True,(255,0,0))
			self.rect.y= 0
			self.rect.x = randint(0 , win_width-self.w)
######################################
class Bullet(GameSprite):
	def __init__(self,img,w,h,x,y,speed):
		GameSprite.__init__(self,img,w,h,x,y,speed)
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y+self.h<0:
			self.kill()
rocket = Player(img="rocket.png",w=50,h=50,x=250,y=450,speed=1)
bullets =sprite.Group()
enemies = sprite.Group()#Создали группу спрайтов врагов
for i in range(5):
	enemy = UFO(img="ufo.png",w=50,h=50,x=randint(0,win_width-50),y=0,speed=1)
	enemies.add(enemy)
while True:
	window.blit(background,(0,0))
	enemies.draw(window)#отрисовка всех спрайтов группы
	enemies.update()#применяем .update() ко всем спрайтам в группе
	bullets.draw(window)
	bullets.update()
	rocket.reset()
	rocket.update()
	#Располагаем надписи "Убито" и "Пропущено" на экране
	window.blit(text_killed,(0,30))
	window.blit(text_lost,(0,50))
	display.update()
	hits = sprite.groupcollide(bullets,enemies,True,True)
	for i in hits:
		kills+=1
		text_killed = font14.render("Убито:"+str(kills),True,(255,0,0))
		enemy = UFO(img="ufo.png",w=50,h=50,x=randint(0,win_width-50),y=0,speed=1)
		enemies.add(enemy)
	#ЕСЛИ убитых больше/равно 10:
		#выводим на середину экрана надпись "Победа"
		#обновляем экран
		#sleep на 2 секунды
		#закрыть программу
	#ЕСЛИ пропущенных больше/равно 10:
		#выводим на середину экрана надпись "Проигрыш"
		#обновляем экран
		#sleep на 2 секунды
		#закрыть программу
	for i in event.get(): 
		if i.type==QUIT:
			quit()
		if i.type == KEYDOWN:
			if i.key == K_SPACE:
				rocket.fire()
	clock.tick(FPS)