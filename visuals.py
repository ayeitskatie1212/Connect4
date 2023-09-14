import pygame
from pygame.locals import *
from Connect4 import Game

game = Game()
SCALE = 100  # overall scale of the board
DEFAULT_WIDTH = game.width  # number of game pieces in a row
DEFAULT_HEIGHT = game.height # number of game pieces in a column
SCREEN_SIZE = DEFAULT_WIDTH * SCALE
DIST_BETWEEN_CIRCLES = SCALE // 5
CIRCLE_RADIUS = (SCREEN_SIZE - (DEFAULT_WIDTH + 1) * DIST_BETWEEN_CIRCLES) // (DEFAULT_WIDTH * 2)

pygame.init()
HEADER_FONT = pygame.font.Font(None, SCALE)
SUBHEADER_FONT = pygame.font.Font(None, SCALE//2)
screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE*DEFAULT_HEIGHT//DEFAULT_WIDTH])

#LAY OUT THE INITIAL STATE OF THE BOARD

def resetGame():
    screen.fill((66, 135, 245))
    for i in range(DEFAULT_WIDTH):
        x = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * i + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
        for j in range(DEFAULT_HEIGHT):
            y = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * j + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
            pygame.draw.circle(screen, (13, 73, 168), (x, y), CIRCLE_RADIUS + 3)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), CIRCLE_RADIUS)
    pygame.display.flip()
resetGame()

def display_ending_message(message):
    draw_text(message, HEADER_FONT, SCREEN_SIZE//2, SCREEN_SIZE//3, 2)
    draw_text("Click anywhere to continue", SUBHEADER_FONT, SCREEN_SIZE//2, SCREEN_SIZE//2, 1)
    pygame.display.update()

def draw_text(words, font, x, y, offset = 1):
    text = font.render(words, True, (0, 0, 0))
    backgroundText = font.render(words, True, (255, 255, 255))
    textrect = text.get_rect()
    textrect.center = (x+offset, y+offset)
    screen.blit(backgroundText, textrect)
    textrect.center = (x-offset, y-offset)
    screen.blit(backgroundText, textrect)
    textrect.center = (x+offset, y-offset)
    screen.blit(backgroundText, textrect)
    textrect.center = (x-offset, y+offset)
    screen.blit(backgroundText, textrect)
    textrect.center = (x, y)
    screen.blit(text, textrect)

gameInProgress = True
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if (gameInProgress):
                xClick, _ = pygame.mouse.get_pos()
                col = xClick // (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES)
                # makes sure it stays in bounds to account for rounding errors
                if (col >= DEFAULT_WIDTH):
                    col = DEFAULT_WIDTH - 1
                result = game.place_chip(col)
                row = game.availableSpots[col] + 1
                if row != -1:
                    x = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * col + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
                    y = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * row + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
                    chipColor = (255, 0, 0) if game.player == 1 else (255, 255, 0)
                    chipColorDark = (120, 10, 0) if game.player == 1 else (120, 120, 0)
                    pygame.draw.circle(screen, chipColorDark, (x, y), CIRCLE_RADIUS)
                    pygame.draw.circle(screen, chipColor, (x, y), CIRCLE_RADIUS - SCALE//20)
                    pygame.display.flip()
                if result != 0:
                    gameInProgress = False
                    if result == 1:
                        display_ending_message("Player 1 has won!")
                    elif result == 2:
                        display_ending_message("Player 2 has won!")
                    elif result == 3:
                        display_ending_message("The game was a tie!")
            else:
                resetGame()
                game.reset_game()
                gameInProgress = True
                
pygame.quit()
    
