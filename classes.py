# -*- coding: utf-8 -*-

import random as r
import pygame 

Source = 'pic/' # folder path where  item and png file are in 

keyboard_input = {pygame.K_DOWN: 'mcgyver.move_y(40)',
                  pygame.K_UP: 'mcgyver.move_y(-40)',
                  pygame.K_LEFT: 'mcgyver.move_x(-40)',
                  pygame.K_RIGHT: 'mcgyver.move_x(40)',}


class AgentScreen:
    # this list of tools needed  in our game (png pictures in pic foder)
    Tool = ['mcgyver', 'mur', 'flor', 'tc', 'pwr',  ]

    def __init__(self):
        #inisialize pyagme
        pygame.init() 
        #Display screen width and height
        self.window = pygame.display.set_mode((600, 600))
        #
        self.font = pygame.font.Font(None, 40)
        self.load_element()

        self.position = self.mcgyver.get_rect()
        self.tc_position = (14*40, 14*40)

        my_Labyr = Labyr()
        self.allowed_flors = my_Labyr.get_map()

        self.objects = [position for position in r.sample(self.allowed_flors, 3)]

    def load_element(self): 
        #loading sprites 

        for pwr in AgentScreen.Tool:
            setattr(self, pwr, pygame.image.load(Source + pwr + ".png").convert_alpha())

    def show_text(self, message):
        self.text = self.font.render((str(message)), 1, (10, 10, 10))
        self.textpos = self.text.get_rect()
        self.window.blit(self.text, self.textpos)

    def show_element(self):
        #
        self.window.blit(self.mur, (0, 0))
        for flor in self.allowed_flors:
            self.window.blit(self.flor, flor)
        for pwr in self.objects:
            self.window.blit(self.pwr, pwr)

        self.show_text(str(len(self.objects)))
        self.window.blit(self.mcgyver, self.position)
        self.window.blit(self.tc, self.tc_position)

    def refresh(self):
        pygame.display.flip()

    def repeat_key(self):
        pygame.key.set_repeat(400, 30)

class ActionGame:
#this class for control the game actions 

    def __init__(self, mcgyver):
        self.mcgyver = mcgyver

    def move_x(self, x):
        next_position = self.mcgyver.position[0] + x, self.mcgyver.position[1]
        if not next_position in self.mcgyver.allowed_flors:
            x = 0
        self.mcgyver.position = self.mcgyver.position.move(x, 0)

    def move_y(self, y):
        next_position = self.mcgyver.position[0], self.mcgyver.position[1] + y
        if not next_position in self.mcgyver.allowed_flors:
            y = 0
        self.mcgyver.position = self.mcgyver.position.move(0, y)

    def check_objects(self):
        pos = (self.mcgyver.position[0], self.mcgyver.position[1])

        if pos in self.mcgyver.objects:
            self.mcgyver.objects.remove(pos)

        if pos == self.mcgyver.tc_position:
            self.check_end_game()
            return False

        return True

    def check_end_game(self):
        if self.mcgyver.objects:
            print('Game Over')
        else:
            print('Bravo!!!!')


class Labyr: 
#generate maze data file
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ok_flors_positions = []

    def read_data_file(self):
        with open('maze', 'r') as my_file:
            data = my_file.read().split('\n')
            return data
        return False

    def get_map(self):
        data = self.read_data_file()

        if data:
            for ordinate, pwr in enumerate(data):
                self.y = ordinate
                for abscisse, letter in enumerate(pwr):
                    if letter == 'O':
                        self.x = abscisse
                        self.ok_flors_positions.append((self.x*40, self.y*40))
            return self.ok_flors_positions


def start_game():

    interface = AgentScreen()
    mcgyver = ActionGame(interface)
    interface.repeat_key()
    continue_game = True

    while 'user playing' and continue_game:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continue_game = False
                if event.key in keyboard_input:
                    eval(keyboard_input[event.key])

        interface.show_element()
        if not mcgyver.check_objects():
            break
        interface.refresh()

if __name__ == '__main__':
    start_game()        
