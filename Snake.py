import time
import random
import pygame
from pygame.locals import *  # import keys

size = 40

class Apple:
    def __init__(self, parent_apple):
        self.parent_apple = parent_apple
        self.x = random.randint(0, 24)*size
        self.y = random.randint(0, 19)*size
        self.apple_block = pygame.image.load('E:/ML/Python/Game/resources/apple.jpg').convert()

    def apple_draw(self):
        self.parent_apple.blit(self.apple_block, (self.x, self.y))
        pygame.display.flip()

    def move_apple(self):
        self.x = random.randint(0, 24)*size
        self.y = random.randint(0, 19)*size

class Snake:
    def __init__(self, parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        # add the block on the screen
        self.block = pygame.image.load('E:/ML/Python/Game/resources/block.jpg').convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'down'

    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_right(self):
        self.direction = 'right'
    def move_left(self):
        self.direction = 'left'

    def snake_walk(self):
        # update body
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'left':
            self.x[0] -= size

        self.snake_draw()

    def snake_draw(self):
        #self.render_background()
        #self.parent_screen.fill((39, 183, 48))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")
        pygame.mixer.init()
        self.play_background()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface,1)
        self.snake.snake_draw()
        self.apple = Apple(self.surface)
        self.apple.apple_draw()

    def is_collision(self, x1, y1, x2,y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length - 1}",True,(255,255,255))
        self.surface.blit(score, (850,10))

    def play_background(self):
        pygame.mixer_music.load('E:/ML/Python/Game/resources/back.mp3')
        pygame.mixer_music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f'E:/ML/Python/Game/resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('E:/ML/Python/Game/resources/background.jpg')
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.snake_walk()
        self.apple.apple_draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with the Apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move_apple()


        #snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")

        # snake colliding with the boundaries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundary error"

    def show_game_over(self):
        self.render_background()
        #self.surface.fill((39, 183, 48))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over!!, Your Score is: {self.snake.length}", True, (199, 16, 16))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press Enter, To Exit press Esc", True, (255,255,255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer_music.pause()



    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer_music.play()
                        pause = False
                    if not pause:
                        if event.key == K_UP and not self.snake.move_up():
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(.2)


if __name__ == "__main__":
    game = Game()
    game.run()


