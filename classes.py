# -*- coding: utf-8 -*-

import random as r
import pygame

Source = 'pic/' # folder path where  item and png file are in

keyboard_input = {pygame.K_DOWN: 'mcgyver.move_y(40)',
                  pygame.K_UP: 'mcgyver.move_y(-40)',
                  pygame.K_LEFT: 'mcgyver.move_x(-40)',
                  pygame.K_RIGHT: 'mcgyver.move_x(40)',}


class AgentScreen:
    #this list of tools needed  in our game (png pictures in pic foder)
    Tool = ['mcgyver', 'mur', 'flor', 'guardian', 'pwr', 'tresor',
            'dim', 'depart', 'xp', 'gameover']

    def __init__(self):
        #inisialize pyagme
        pygame.init()
        #Display screen width and height
        self.window = pygame.display.set_mode((600, 600))
        #fontsize
        self.font = pygame.font.Font(None, 60)
        self.load_element()
        #display start,xp,mcgyver,guardian and  position
        self.position = self.mcgyver.get_rect()
        self.mcgyver_position = (0*40, 1*40)
        self.depart_position = (0*40, 1*40)
        self.guardian_position = (14*40, 14*40)
        self.xp_position = (1*40, 0*40)


        my_Labyr = Labyr()
        self.allowed_flors = my_Labyr.get_map()

        # generate 3 random object coordinates
        self.objects = [position for position in r.sample(self.allowed_flors, 3)]
        self.obj_pwr = self.objects[0]
        self.obj_tresor = self.objects[1]
        self.obj_dim = self.objects[2]

    def load_element(self):
        #loading sprites
        for pwr in AgentScreen.Tool:
            setattr(self, pwr, pygame.image.load(Source + pwr + ".png").convert_alpha())

    def show_text(self, message):
    	#Show remaining item on the top left
        self.text = self.font.render((str(message)), 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.window.blit(self.text, self.textpos)

    def show_element(self):
        self.window.blit(self.mur, (0, 0))
        # show the maze path
        for flor in self.allowed_flors:
            self.window.blit(self.flor, flor)
        # show  tools that will be taken by Mcgyver
        object_types = {self.obj_pwr: 'self.window.blit(self.pwr, obj)',
                        self.obj_tresor: 'self.window.blit(self.tresor, obj)',
                        self.obj_dim: 'self.window.blit(self.dim, obj)'}
        for obj in self.objects:
            eval(object_types[obj])

        #display start,xp,mcgyver,guardian
        self.show_text(str(len(self.objects)))
        self.window.blit(self.depart, self.depart_position)
        self.window.blit(self.mcgyver, self.position)
        self.window.blit(self.guardian, self.guardian_position)
        self.window.blit(self.xp, self.xp_position)



    def refresh(self):
    	#Clean all graphics elements
        pygame.display.flip()

    def repeat_key(self):
        #Move few times character when key pressed for a long time
        pygame.key.set_repeat(400, 30)

class ActionGame:
#this class for control the game actions

    def __init__(self, mcgyver):
        self.mcgyver = mcgyver

    def move_x(self, x):
    	#Manage horizontal moves'''
        # check next coordinates if are allowed
        next_position = self.mcgyver.position[0] + x, self.mcgyver.position[1]
        if not next_position in self.mcgyver.allowed_flors:
        	# if not, Mcgyver not move
            x = 0
        self.mcgyver.position = self.mcgyver.position.move(x, 0)

    def move_y(self, y):
    	#Manage vertical moves'''
        next_position = self.mcgyver.position[0], self.mcgyver.position[1] + y
        if not next_position in self.mcgyver.allowed_flors:
            y = 0
        self.mcgyver.position = self.mcgyver.position.move(0, y)

    def check_objects(self):
    	#When Mcgyver is next to a chest, that remove item
        pos = (self.mcgyver.position[0], self.mcgyver.position[1])
        # compare Mcgyver position with objects
        if pos in self.mcgyver.objects:
        	# delete item when taken
            self.mcgyver.objects.remove(pos)

        # compare Mcgyver position with guardian position
        if pos == self.mcgyver.guardian_position:
            self.check_end_game()
            # end game
            return False
        # continue game
        return True

    def check_end_game(self):
    	#When Mcgyver is next to guardian that check if Mcgyver have all items
        if self.mcgyver.objects:
            print('gameover')
        else:
            print('Bravo!!!!')


class Labyr:
#generate maze data file
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ok_flors_positions = []

    def read_data_file(self):
    	#Get level of labyrinth from data file
        with open('maze', 'r') as my_file:
            data = my_file.read().split('\n')
            return data
        # if fail to read file
        return False

    def get_map(self):
    	#Convert data file into list of coordinates
        data = self.read_data_file()

        if data:
            for ordinate, pwr in enumerate(data):
                self.y = ordinate
                for abscisse, letter in enumerate(pwr):
                    if letter == 'O': # O = free way
                        self.x = abscisse
                        self.ok_flors_positions.append((self.x*40, self.y*40))
                    elif letter == 'd': # d = start
                        self.x = abscisse
                        self.ok_flors_positions.append((self.x*40, self.y*40))
                    elif letter == 'a': # a = depart
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
        	# waiting input key from user
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                	# end game when pressed escape key
                    continue_game = False
                if event.key in keyboard_input:
                    eval(keyboard_input[event.key])

        interface.show_element()
        if not mcgyver.check_objects():
        	# when Mcgyver is next to the guardian, the game ends
            break
        interface.refresh()


if __name__ == '__main__':
    start_game()
