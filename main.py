import random
import sys
import pygame 
import spritesheet
from pygame import mixer

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = IMAGE
        self.rect = self.image.get_rect(center=pos)

# Extracting all modes of character from spritesheet. (Walking, running, jumping, etc.)
def addDinoAnimations():
	global animations
	sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
	sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
	stepCounter = 0 
	animationSteps = [4, 6, 3, 4, 7]
	for animation in animationSteps:
		tempList = []
		for _ in range(animation):
			tempList.append(sprite_sheet.get_image(stepCounter, 24, 24, 5, (0, 0, 0)))
			stepCounter += 1
		animations.append(tempList)

def addEnemyAnimations():
	global enemyAnimations
	enemySpriteSheetImage = pygame.image.load('enemy2.png').convert_alpha()
	eSpriteSheet = spritesheet.SpriteSheet(enemySpriteSheetImage)
	for i in range(5):
		enemyAnimations.append(eSpriteSheet.get_image(i, 24, 24, 6, (0, 0, 0)))

def gameScreen():
	global gameActive
	global score
	gameActive = True
	fontType = 'snapitc'
	fontSize = 64
	background = pygame.image.load('grass.jpg')
	scoreFont = pygame.font.SysFont(fontType, fontSize)
	scoreText = scoreFont.render('Score: ' + str(score), True, pygame.Color('red'))
	storeFont = pygame.font.SysFont(fontType, fontSize)
	storeText = storeFont.render('Store' , True , pygame.Color('red'))
	screen.blit(background, (0, 0))
	screen.blit(scoreText, (0, 0))
	screen.blit(storeText, (SCREEN_WIDTH - 256, 0))

#print(pygame.font.get_fonts())
def homeScreen():
	global SCREEN_WIDTH
	global SCREEN_HEIGHT
	background = pygame.image.load('grass.jpg')
	fontType = 'snapitc'
	fontSize = 128
	titleScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_WIDTH))
	title = pygame.font.SysFont(fontType, fontSize)
	titleText = title.render('Dino Runner', True, pygame.Color('red'))
	titleRect = titleText.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//10))
	subTitle = pygame.font.SysFont(fontType, fontSize//3)
	subTitleText = subTitle.render('Press D or the right arrow key to start', True, pygame.Color('red'))
	subTitleRect = subTitleText.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
	titleScreen.blit(background, (0, 0))
	titleScreen.blit(titleText, titleRect)
	titleScreen.blit(subTitleText, subTitleRect)
	screen.blit(titleScreen, (0, 0))

def displayStore():
	global SCREEN_WIDTH
	global SCREEN_HEIGHT
	global dinoCounter
	global dinoCost
	dinoCost = round(((20 * dinoCounter)/(1/3)) + pow(dinoCounter, 3))
	fontType = 'snapitc'
	fontSize = 128
	fontColor = pygame.Color('black')
	storeScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_WIDTH))
	storeScreen.fill(pygame.Color('grey'))
	title = pygame.font.SysFont(fontType, fontSize)
	titleText = title.render('Store', True, fontColor)
	titleRect = titleText.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//10))
	exitStoreFont = pygame.font.SysFont(fontType, fontSize//2)
	exitStoreText = exitStoreFont.render('X' , True , fontColor)
	buyDinoF = pygame.font.SysFont(fontType, fontSize//3)
	buyDinoT = buyDinoF.render('Buy another dino! Current number of dinos: ' + str(dinoCounter), True, fontColor)
	buyDinoR = buyDinoT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
	dinoButton = buyDinoF.render('Purchase one for: ' + str(dinoCost) , True , fontColor)
	dinoButtonR = dinoButton.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
	storeScreen.blit(exitStoreText, (SCREEN_WIDTH - 192, 0))
	storeScreen.blit(buyDinoT, buyDinoR)
	storeScreen.blit(dinoButton, dinoButtonR)
	storeScreen.blit(titleText, titleRect)
	screen.blit(storeScreen, (0, 0))

def gameOverScreen():
	fontType = 'snapitc'
	fontSize = 128
	gOFont = pygame.font.SysFont(fontType, fontSize)
	gOText = gOFont.render("GAME OVER!", True, (255, 255, 255))
	screen.fill(pygame.Color('black'))
	screen.blit(gOText, (SCREEN_WIDTH//8, SCREEN_HEIGHT//3))

def dinoFrames():
	global prevTime
	global cd
	global frame
	global action
	global animations
	global dinoY 
	global jumping
	currentTime = pygame.time.get_ticks()
	if currentTime - prevTime >= cd:
		frame += 1
		prevTime = currentTime
		if jumping and frame >= len(animations[action]):
			jumping = not jumping
			action = 1
			cd = 100
		if frame >= len(animations[action]) and action != 0:
			frame = 0
			action = 1
			cd = 100
		if action == 2 and frame < 2:
			dinoY -= 100
		elif action == 2 and frame >= 2:
			dinoY += 100
		if frame >= len(animations[action]):
			frame = 0
			action = 0
			cd = 100

def enemyFrames():
	global enemyPrevTime
	global enemyFrame
	global enemyCD 
	global enemyAnimations
	currTime = pygame.time.get_ticks()
	if currTime - enemyPrevTime >= enemyCD:
		enemyFrame += 1
		enemyPrevTime = currTime
		if enemyFrame >= len(animations):
			enemyFrame = 0


def coinCollision():
	global coin
	global action
	if coin.rect.x <= dinoX and action != 2 and dinoY == coinY:
		return True
	elif coin.rect.x <= dinoX and action == 2:
		coin.rect.x = random.randint(1500, 1600)
		return False
	else:
		return False

def enemyCollision():
	global dinoX
	global dinoY
	global enemyX
	global enemyY
	global action
	global gameOver 
	global gameActive
	global gameEndTime
	if enemyX <= dinoX and enemyY == dinoY and action != 2:
		gameEndTime = pygame.time.get_ticks()
		gameOverScreen()
		gameOver = True
		gameActive = False
		return True
	elif enemyX <= dinoX and action == 2:
		enemyX = random.randint(2500, 3000)
		return False
	else:
		return False

def makeCoin():
	global coin
	global activeCoin
	activeCoin = True
	coinX = random.randint(1500, 1600)
	coin = Coin((coinX, coinY))

def coinFrames():
	global activeCoin
	global coin
	global score
	global dinoCounter
	coinCD = 500
	startTime = 0
	currTime = pygame.time.get_ticks()
	if currTime >= startTime:
		startTime = currTime + coinCD
		coin.rect.x -= 10
		if coinCollision():
			activeCoin = False
			score += 100 * dinoCounter 
			collision_sound = mixer.Sound('coinsound.wav')
			collision_sound.play()
			collision_sound.set_volume(.15)

def main():
	global prevTime
	global cd
	global frame
	global action
	global gameActive
	global dinoY 
	global dinoX
	global activeCoin
	global coin
	global score
	global activeStore 
	global dinoCounter 
	global dinoCost
	global enemyX
	global enemyY
	global enemyAnimations
	global enemyFrame
	global jumping
	global gameOver 
	global gameEndTime 
	gameEndCD = 5000
	gameOver = False
	jumping = False
	dinoCost = 50
	dinoCounter = 1
	activeStore = False
	score = 0
	dinoY = 500
	dinoX = 0
	run = True
	while run:  
		# Background color.
		screen.fill((50, 50, 50))
		if gameOver:
			currTime = pygame.time.get_ticks()
			if currTime - gameEndTime >= gameEndCD:
				pygame.quit()
				sys.exit()
			gameOverScreen()

		# Game/home/store screen.
		if not activeStore and not gameActive and not gameOver:
			homeScreen()
		elif not activeStore and gameActive and not gameOver:
			gameScreen()
			# Coin generator and animations.
			if not activeCoin:
				makeCoin()
			elif activeCoin and gameActive:
				coinFrames()
				screen.blit(coin.image, (coin.rect.x, coinY))
		elif activeStore and not gameOver:
			displayStore()

		# Animations for dino.
		if activeStore and not gameOver:
			dinoFrames()
			enemyFrames()
		elif not gameOver:
			dinoFrames()
			screen.blit(animations[action][frame], (dinoX, dinoY))

		if gameActive and not activeStore and not gameOver:
			enemyFrames()
			if not enemyCollision():
				enemyX -= 10
			screen.blit(enemyAnimations[enemyFrame], (enemyX, enemyY))

		# Game loop.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if not gameOver and event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
					run = False
				if not jumping:
					if (event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w) and gameActive:
						action = 2
						cd = 200
						frame = 0
						jumping = not jumping
				if (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
					action = 1
					cd = 100
					frame = 0
					gameActive = True
				if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and gameActive:
					action = 4
					cd = 150
					frame = 0
				if (event.key == pygame.K_TAB):
					if gameActive:
						if activeStore:
							activeStore = not activeStore
						else:
							activeStore = True
							displayStore()
			if not gameOver and event.type == pygame.MOUSEBUTTONDOWN:
				mouse = pygame.mouse.get_pos()
				if SCREEN_WIDTH - 256 <= mouse[0] <= SCREEN_WIDTH and 0 <= mouse[1] <= 70:
					if gameActive:
						if activeStore:
							activeStore = not activeStore
						else:
							activeStore = True
							displayStore()
				if activeStore and score - dinoCost >= 0 and 0 <= mouse[0] <= SCREEN_WIDTH and SCREEN_HEIGHT // 3 <= mouse[1] <= (SCREEN_HEIGHT // 3) + 80:
					score -= dinoCost
					dinoCounter += 1
		pygame.display.flip()
	pygame.quit()

if __name__ == '__main__':
	pygame.init()
	global SCREEN_WIDTH
	global SCREEN_HEIGHT
	global screen
	global animations
	global action
	global cd
	global frame
	global prevTime
	global gameActive
	global IMAGE
	global activeCoin
	global PATH 
	global enemyAnimations
	global enemyX
	global enemyPrevTime
	global enemyFrame
	global enemyCD 
	global coinY
	coinY = 500
	enemyCD = 200
	enemyFrame = 0
	enemyX = random.randint(2500, 3000)
	enemyY = 500
	enemyAnimations = []
	PATH = './Pygame/DinoRunner/'
	activeCoin = False
	prevTime = pygame.time.get_ticks()
	enemyPrevTime = pygame.time.get_ticks()
	gameActive = False
	animations = [] # All types of animations (running, walking, jumping, etc)
	action = 0 # Different modes of character.
	cd = 100 # How fast/slow the animation is.
	frame = 0 # Which frame of the action the animation is in.
	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 720
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Dino Runner')
	IMAGE = pygame.image.load('coin128.png').convert_alpha()
	addDinoAnimations()
	addEnemyAnimations()
	main()