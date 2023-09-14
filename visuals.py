import pygame
from pygame.locals import *
from Connect4 import Game

game = Game()
SCALE = 100  # overall scale of the board
SCREEN_SIZE = game.width * SCALE

# Logic to create an evenly spaced board
DIST_BETWEEN_CIRCLES = SCALE // 5
CIRCLE_RADIUS = (SCREEN_SIZE - (game.width + 1) * DIST_BETWEEN_CIRCLES) // (game.width * 2)

pygame.init()
HEADER_FONT = pygame.font.Font(None, SCALE)
SUBHEADER_FONT = pygame.font.Font(None, SCALE//2)
screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE*game.height//game.width])

 # Resets the screen to the basic board layout
def resetGame():
    screen.fill((66, 135, 245))
    for i in range(game.width):
        x = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * i + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
        for j in range(game.height):
            y = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * j + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
            pygame.draw.circle(screen, (13, 73, 168), (x, y), CIRCLE_RADIUS + 3)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), CIRCLE_RADIUS)
    pygame.display.flip()
resetGame()

def display_ending_message(message):
    draw_text(message, HEADER_FONT, SCREEN_SIZE//2, SCREEN_SIZE//3, 2)
    draw_text("Click anywhere to continue", SUBHEADER_FONT, SCREEN_SIZE//2, SCREEN_SIZE//2, 1)
    pygame.display.update()

 # Draws black text with a white border
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

onEndScreen = False
running = True
while running:
    for event in pygame.event.get():
        # Close the window if the user presses the x button
        if event.type == QUIT:
            running = False
        # Close the window if the user presses the escape key
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            # If the game is over, clicking anywhere will reset the game
            if onEndScreen:
                resetGame()
                game.reset_game()
                onEndScreen = False
            else:
                xClick, _ = pygame.mouse.get_pos()
                # Calculate the column that the user clicked in
                col = xClick // (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES)
                # makes sure it stays in bounds to account for rounding errors
                if (col >= game.width):
                    col = game.width - 1
                
                # Play the round and get the result
                result = game.place_chip(col)
                row = game.availableSpots[col] + 1

                # If the user clicked on a valid spot, draw the chip
                # Example of an invalid spot would be when the column is full
                if row != -1:
                    # Calculate the x and y of where the chip should go based off of the row and column of placement
                    x = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * col + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
                    y = (CIRCLE_RADIUS * 2 + DIST_BETWEEN_CIRCLES) * row + CIRCLE_RADIUS + DIST_BETWEEN_CIRCLES
                    # Draw the chip
                    chipColor = (255, 0, 0) if game.player == 1 else (255, 255, 0)
                    chipColorDark = (120, 10, 0) if game.player == 1 else (120, 120, 0)
                    pygame.draw.circle(screen, chipColorDark, (x, y), CIRCLE_RADIUS)
                    pygame.draw.circle(screen, chipColor, (x, y), CIRCLE_RADIUS - SCALE//20)
                    pygame.display.flip()

                # If the game is over, display the ending message
                if result != 0:
                    onEndScreen = True
                    if result == 1:
                        display_ending_message("Player 1 has won!")
                    elif result == 2:
                        display_ending_message("Player 2 has won!")
                    elif result == 3:
                        display_ending_message("The game was a tie!")      
pygame.quit()
    
