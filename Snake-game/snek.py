import pygame
import random
import tkinter
from tkinter import messagebox
import time
pygame.init()




class Cube():
	
	rows = 20
	w = 500

	def __init__(self,start,dirnx=1,dirny=0,color = (255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self,dirnx,dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0]+self.dirnx, self.pos[1] + self.dirny)

	def draw(self,surface,eyes=False):
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface,self.color, (i*dis+1,j*dis+41, dis-2,dis-2))
		if eyes:
		 	centre = dis // 2
		 	radius = 3
		 	eye1 = (i*dis + centre - radius,j*dis+49)
		 	eye2 = (i*dis + centre + radius,j*dis+49)
		 	pygame.draw.circle(surface, (0,0,0), eye1, radius)
		 	pygame.draw.circle(surface, (0,0,0), eye2, radius)





class Snake():
	body = []
	turns = {}
	score = 0

	def __init__(self,color, pos):
		self.color = color
		self.head = Cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1

	def move(self):

		keys = pygame.key.get_pressed()

		
		if keys[pygame.K_a]:
			self.dirny = 0
			self.dirnx = -1
			self.turns[self.head.pos] = [self.dirnx,self.dirny]

		elif keys[pygame.K_d]:
			self.dirny = 0
			self.dirnx = 1
			self.turns[self.head.pos] = [self.dirnx,self.dirny]

		elif keys[pygame.K_w]:
			self.dirny = -1
			self.dirnx = 0
			self.turns[self.head.pos] = [self.dirnx,self.dirny]

		elif keys[pygame.K_s]:
			self.dirny = 1
			self.dirnx = 0
			self.turns[self.head.pos] = [self.dirnx,self.dirny]
		
		for i, c in enumerate(self.body):
			
			p = c.pos
			
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				if c.dirnx == -1 and c.pos[0] <= 0:
					c.pos = (c.rows-1,c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
					c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1:
					c.pos = (c.pos[0],0)
				elif c.dirny == -1 and c.pos[1] <= 0:
					c.pos = (c.pos[0] , c.rows-1)
				else:
					c.move(c.dirnx,c.dirny)


	def reset(self,pos):
		self.head = Cube(pos)
		self.body = []
		self.turns = {}
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1
		self.score = 0

	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny
		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1]-1 )))
		elif dx == 0 and dy == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy


	def draw(self,surface):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)






def drawGrid(w,rows,surface):
	size = w // rows
	x = 0
	y = 40
	#for i in range(rows):
		#x += size
		#y += size

	#pygame.draw.line(surface, (255,255,255), (x,40), (x,w+40))
	pygame.draw.line(surface, (255,255,255), (0,y), (w,y))


def updateHighScore(fileName,score):
	try:
		with open(fileName,'r+') as file:
			content = file.read()
			if int(content) < score:
				file.seek(0)
				file.truncate()
				file.write(str(score))
				return score
			return int(content)

	except:
		file = open(fileName,'w')
		file.write('0')
		file.close()
		return 0



def redrawWindow(surface):
	global rows, width
	
	text = font1.render('Score: '+ str(s.score), 1,(255,255,255))
	text1 = font1.render("SNEK gaem", 1, (255,255,255))
	hs = font1.render("HS: " + str(highScore), 1, (255,255,255))

	surface.fill((0,0,0))
	

	#r = text1.get_rect()
	#r.center = (200,10)
	#pygame.draw.rect(surface, (0,255,0),(200,10,r[2],r[3]))
	#pygame.draw.rect(surface,(0,255,0),r)


	win.blit(text, (400,10))
	win.blit(text1, (200,10))
	win.blit(hs, (20,10))

	drawGrid(width,rows,surface)
	s.draw(surface)
	snack.draw(surface)
	pygame.display.update()



def randomSnack(rows, item):
	
	pos = item.body


	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z: z.pos == (x,y), pos))) > 0:
			continue
		else:
			break

	return (x,y)




def message_box(subject, content):
	root = tkinter.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass







def main():
	global rows,width, s, snack, font1,win, highScore
	#pygame.font.init()
	
	font1 = pygame.font.Font('sans.ttf', 20)
	height = 540
	width = 500
	rows = 20
	
	win = pygame.display.set_mode((width,height))
	pygame.display.set_caption("Snek")
	s = Snake((255,0,0) , (10,10))
	snack = Cube(randomSnack(rows, s), color = (0,255,0))
	
	


	highScore = str(updateHighScore('hs.txt',s.score))

	flag = True
	clock = pygame.time.Clock()
	try:
		
		while flag:
			pygame.time.delay(100)
			clock.tick(15)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					#flag = False
					pygame.quit()
			

			s.move()
			
			if s.body[0].pos == snack.pos:
				s.addCube()
				s.score+=1
				snack = Cube(randomSnack(rows, s), color = (0,255,0))

			if s.body[0].pos in list(map(lambda x:x.pos,s.body[1:])):
				print("you ded")
				hit.play()
				message_box("You lost", "Score:" + str(len(s.body)-1))
				highScore = str(updateHighScore('hs.txt',s.score))
				s.reset((10,10))

			
			redrawWindow(win)
	except pygame.error:
		pass




pygame.mixer.music.set_volume(0.09)
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)


hit = pygame.mixer.Sound("hit1.wav")
hit.set_volume(0.1)




main()
