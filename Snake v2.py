import sys, pygame, math
import time as time
from random import randrange
from pygame.locals import *

class Snake:

    def __init__(self):
        self.size = width, height = 324, 576
        self.inputs = {"up":pygame.K_UP,"down":pygame.K_DOWN, "left":pygame.K_LEFT, "right":pygame.K_RIGHT}
        self.objects = {}
        self.object_locations = {}
        self.time_delay = 0.1
        self.bg_color = 0, 0, 0
        self.block_size = 16
        self.goal_limits = [1, 20, 36]

        self.new_block_name = 1
        self.last_input = ""
        self.time_save = 0
        self.score = 0
        self.hit = False

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("SNAKE")

        self.make_first_blocks()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            if self.hit == True:
                    self.end()
                    break
            
            self.input_test()
            self.move_block()
            self.test_walls()
            self.test_tail()
            self.goal_test()

            self.screen.fill(self.bg_color)
            for object_name in self.objects:
                self.screen.blit(self.objects[object_name][0], self.objects[object_name][1])
                
            pygame.display.flip()

    def end(self):
        screen = pygame.display.set_mode((350, 30))
        pygame.display.set_caption('Basic Pygame program')

        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))

        font = pygame.font.Font(None, 36)
        lost ="GAME OVER!   Score : {}".format(str(self.score))
        text = font.render(lost, 5, (100, 100, 100))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

        screen.blit(background, (0, 0))
        pygame.display.flip()

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            screen.blit(background, (0, 0))
            pygame.display.flip()

    def make_first_blocks(self):
        self.goal_block_load = pygame.image.load("goal.png")
        self.goal_block = self.goal_block_load.get_rect()

        range_limit = self.goal_limits

        self.goal_block[0] = randrange(range_limit[0], range_limit[1])*16
        self.goal_block[1] = randrange(range_limit[0], range_limit[2])*16
        self.objects["goal"] = [self.goal_block_load, self.goal_block]

        self.head_block_load = pygame.image.load("block_head.png")
        self.head_block = self.head_block_load.get_rect()
        self.objects["0"] = [self.head_block_load, self.head_block]
        self.head_block[0] = 16
        self.head_block[1] = 16
 
    def input_test(self):
        self.key = pygame.key.get_pressed()

        try:
            test = self.key.index(1)

        except ValueError:
            dummy = True

        else:
            for input_name in self.inputs:
                inp = self.inputs[input_name]
                if self.key[inp] == 1:
                    self.last_input = input_name

    def move_block(self):
        if self.last_input != "":

            if time.time() > self.time_save + self.time_delay or self.time_save == 0:
                
                self.save_locations()

                if self.last_input == "up":
                    self.head_block[1] -= self.block_size
                    
                elif self.last_input == "down":
                    self.head_block[1] += self.block_size

                elif self.last_input == "left":
                    self.head_block[0] -= self.block_size
                    
                elif self.last_input == "right":
                    self.head_block[0] += self.block_size

                self.time_save = time.time()

                for block in self.objects:
                    if block != "goal" and block != "0":  
                        self.move_tail(block)    

    def save_locations(self):
        for block in self.objects:
            block_data = self.objects[block][1]
            first_coord = block_data[0]
            second_coord = block_data[1]
            self.object_locations["{}".format(block)] = [first_coord, second_coord]

    def move_tail(self, block):
        block_data_this_all = self.objects[block]
        block_data_this = block_data_this_all[1]
        previus_block_name = str(int(block)-1)

        self.block_location_previus_1 = self.object_locations[previus_block_name][0]
        self.block_location_previus_2 = self.object_locations[previus_block_name][1]

        block_data_this[0] = self.block_location_previus_1
        block_data_this[1] = self.block_location_previus_2

    def goal_test(self):
        if self.head_block == self.goal_block:
            range_limit = self.goal_limits
            self.goal_block[0] = randrange(range_limit[0], range_limit[1])*16
            self.goal_block[1] = randrange(range_limit[0], range_limit[2])*16

            color_1 = randrange(0,255)
            color_2 = randrange(0,255)
            color_3 = randrange(0,255)

            self.bg_color = color_1, color_2, color_3
            self.score += 1
            self.make_new_block()

    def make_new_block(self):
        block_name = str(self.new_block_name)
        self.new_block_load = pygame.image.load("block_tail.png")
        self.new_block = self.head_block_load.get_rect()

        self.objects["{}".format(block_name)] = [self.new_block_load, self.new_block]
        
        self.move_tail(block_name)

        self.new_block[0] = self.block_location_previus_1
        self.new_block[1] = self.block_location_previus_2
        self.new_block_name += 1
         
    def test_walls(self):
        if self.head_block.left < self.goal_limits[0]*16 or self.head_block.right > self.goal_limits[1]*16:
            self.hit = True
            
        if self.head_block.top < self.goal_limits[0]*16 or self.head_block.bottom > self.goal_limits[2]*16:
            self.hit = True
    def test_tail(self):
        for block in self.objects:
            if block != "goal" and block != "0": 
                block_data = self.objects[block][1]
                if block_data == self.head_block:
                    self.hit = True

main = Snake()
main.run()