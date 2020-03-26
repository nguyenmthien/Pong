import pygame, sys

# General setup
pygame.init() 
clock = pygame.time.Clock()
    
# Main Window
screen_width = 800   # width and height of main window
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height)) # screen display 
pygame.display.set_caption('Pong')  #caption

# Colors
light_grey = (200,200,200)  # color for assets
bg_color = pygame.Color('black') # black background

# Game Rectangles
ball = pygame.Rect(int(screen_width / 2 - 15), int(screen_height / 2 - 15), 30, 30) # set initial position of ball
player = pygame.Rect(int(screen_width - 20), int(screen_height / 2 - 70), 10,140) # set initial position of player1, rhs
opponent = pygame.Rect(10, int(screen_height / 2 - 70), 10,140) # set initial position of player2

if __name__ == "__main__": 
    # allow input, currently only allow quit input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# Visuals 
	screen.fill(bg_color) # fill background color
	pygame.draw.rect(screen, light_grey, player) # draw player 1 
	pygame.draw.rect(screen, light_grey, opponent) # draw player 2
	pygame.draw.ellipse(screen, light_grey, ball)  # draw ball 
	pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
    # draw middle line
	pygame.display.flip() #for updating content of the entire display
	clock.tick(60) # allowing 60fps visual 
