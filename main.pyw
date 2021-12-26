import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'
import pygame
from colors import Color as c
from random import randint
from images import guess, create_reference_image

class Text():
    def __init__(self, screen, text, color, dimensions):
        pygame.font.init()
        self.screen = screen
        self.dimensions = dimensions
        self.color = color
        self.font = pygame.font.SysFont('arial', dimensions[1])
        self.label = self.font.render(text, True, color)
        self.screen.blit(self.label, self.dimensions[0])

class Board():
    def __init__(self, surface, size, pixels=20, x=0, y=0):
        self.screen = surface
        self.dimensions = (x, y, size)
        self.grid_size = pixels
        self.PPB = size/pixels
        self.create_board()        
        self.draw_board()

    def create_board(self):
        self.pixels = []
        for _ in range(self.grid_size):
            row = []
            for _ in range(self.grid_size):
                row.append(c["WHITE"])
            self.pixels.append(row)
    
    def draw_board(self):
        self.frame = pygame.draw.rect(self.screen, c["WHITE"], pygame.Rect(*self.dimensions, self.dimensions[2]))
        x, y = self.dimensions[:2]
        for row in self.pixels:
            for col in row:
                pygame.draw.rect(self.screen, col, pygame.Rect(x, y, self.PPB, self.PPB))
                x += self.PPB
            x = self.dimensions[0]
            y += self.PPB

    def compute_coords(self, mouse_pos):
        xPos, yPos = mouse_pos
        if xPos < self.dimensions[2] and yPos < self.dimensions[2]:
            row = (xPos+self.PPB)//self.PPB
            col = (yPos+self.PPB)//self.PPB
        else:
            row, col = (0, 0)
        return (int(row), int(col))
                
class Window():
    def __init__(self, width=400, height=400):
        pygame.init()
        pygame.display.set_caption("AI Guesser")
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.board = Board(self.screen, 400, )
        self.results = []
    
    def main(self):
        run = True
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1500)
        while run:
            clock.tick(60)
            self.screen.fill(c["BLACK"])
            self.board.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        row, col = self.board.compute_coords(pygame.mouse.get_pos())
                        self.board.pixels[col-1][row-1] = c["BLACK"]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.key.key_code("delete"):
                        self.board.create_board()
                    elif event.key == pygame.key.key_code("end"):
                        create_reference_image()
                elif event.type == pygame.USEREVENT:
                    pygame.image.save(self.screen.subsurface(self.board.frame), "board.png")
                    self.results = guess("board.png")

            y = 40
            for result in self.results:
                Text(self.screen, f"{result[0]}: {result[1]}", c["WHITE"], ((410, y), 38))
                y += 45

            Text(self.screen, str(self.board.compute_coords(pygame.mouse.get_pos())), c["WHITE"], ((410, 10), 20))
            pygame.display.flip()

        # os.remove("board.png")
        pygame.quit()

if __name__ == "__main__":
    w = Window(550, 400)
    w.main()
