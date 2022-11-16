import pygame
import json
from pygame.constants import BLEND_ALPHA_SDL2

from pygame.time import Clock
from game import Game
from game_button import GameBtn
from scoreboard import Scoreboard
background_image = pygame.image.load("Assets/gameScreen_bg.png")
background_image = pygame.transform.scale(background_image, (1400,800))

################################################
# Game Screen Class
# Functions:
# __init__(WIN, FPS):
# @params: WIN, FPS
# WIN refers to the window that is displaying to the user
# FPS is how many frames per second the game screen will refresh
# @brief: function initalizes the game screen self variables
# @return: none
# 
# load_progress(bananas,username):
# @params: bananas, username
# bananas refer to the number of bananas the account that has just logged in
# username is the account that just logged in
# @brief: initalises the banana and username to self variables in which will be
# drawn to the screen with # of bananas and the username will be used for saving
# @returns: none
#
# load_accounts():
# @params: none
# @brief: loads up accounts from user_details.txt and them into a list in dictionary form
# @returns: the list of accounts in user_details.txt in dictionary form
#
# save_progress():
# @params: none
# @brief: takes the list of accounts in dictionary form from the function load_accounts()
# and reads in lines from the user_details.txt and corresponds the line number of the username
# with the lines in the user_details.txt and then json dumps the account onto the specific line
# in user_details.txt and saves it as a string and rewrites the previous data of that account with
# the current number of bananas in the sessions
# @returns: none
#
# runGame():
# @params: none
# @brief: initalizes Game class and BananaBtn class and runs in a while loop
# taking all events occuring on the screen and calling methonds corresponding to
# the events. Also auto saves on exit, and in game
# @returns: none
#
# draw_screen(bananaBtn,game):
# @params: bananaBtn,game
# bananaBtn is the main button on the screen in which the user clicks
# game is the Game Class in which handles all of calculations of number of bananas added
# @breif: draws the # number of bananas on the screen along with the leader board and banana button
# @returns: none
##############################################################################

class Game_Screen:
    def __init__(self,WIN,FPS):
        self.FONT = pygame.font.Font(None, 32)
        self.WIN = WIN
        self.run = True
        self.bananas = 0
        self.multiClicks = 0
        self.username = ""
        self.FPS = FPS
        background_image.convert(WIN)
        self.clock = pygame.time.Clock()
        self.board = Scoreboard(1255,10,135,120, "Leader Board")
        
    def load_progress(self,bananas,username,multiClicks):
        self.bananas = bananas
        self.username = username
        self.multiClicks = multiClicks

    
    def load_accounts():
        data = open("user_details.txt","r")
        account_list = []
        for account in data:
            if(account != ""):
                dict_account = json.loads(account)
                account_list.append(dict_account)
        data.close()
        return account_list

    def save_progress(self):
        #print(self.bananas)
        data = open("user_details.txt","r")
        account_list = self.load_accounts()
        list_of_lines = data.readlines()
        lineNum = 0
        saved_account = {}
        for account in account_list:
            if(account["username"] == self.username):
                saved_account = account
                account["bananas"] = self.bananas
                account["multiClicks"] = self.multiClicks
                break
            lineNum += 1
        if(lineNum == len(account_list)-1):
            list_of_lines[lineNum] = json.dumps(saved_account)
        else:
            list_of_lines[lineNum] = json.dumps(saved_account) + "\n"
        data = open("user_details.txt", "w")
        data.writelines(list_of_lines) 
        data.close()
        data.close()
    
    def runGame(self):
        game = Game(self.bananas,self.multiClicks)
        bananaBtn = GameBtn("banana_button",20,70,250,250,"Assets/banana_image.png","Assets/mouseBtn_down.mp3","Assets/mouseBtn_up.mp3")
        multiclick = GameBtn("multiclick_button",500,250,25,25,"Assets/multiClick.png","Assets/mouseBtn_down.mp3","")
        button_list = [bananaBtn,multiclick]
        while self.run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_progress()
                    self.run = False
                #------all button events will be in here------#
                for buttons in button_list:
                    buttons.on_click(event)
            for button in button_list:
                if(button.button_name == "banana_button"):
                    if(button.active == True):
                        game.addBanana()
                        self.bananas = game.bananas
                        button.active = False
                if(button.button_name == "multiclick_button"):
                    if(button.active == True):
                        game.multiClick()
                        self.multiClicks = game.clickMultiplier
                        self.bananas = game.bananas
                        button.active = False
            self.save_progress()
            self.draw_screen(button_list,game)


    def draw_screen(self,button_list,game):
        label_colors = (0,0,0)
        self.WIN.blit(background_image,background_image.get_rect(topleft=(0,0)))
        #anything draw to the screen
        for button in button_list:
            button.draw_button(self.WIN)
        counter_title = "Bananas: " + str(game.bananas)
        counter_surface = self.FONT.render(counter_title, True, label_colors)
        upgrade_title = "MultiClick: +" + str(game.clickMultiplier)
        upgradeCost_title = "Cost: " + str(game.upgradeCost)
        upgradeCost_surface = self.FONT.render(upgradeCost_title, True, label_colors)
        
        upgrade_surface = self.FONT.render(upgrade_title, True, label_colors)
        self.WIN.blit(upgradeCost_surface, (530,250))
        self.WIN.blit(upgrade_surface, (500, 220))
        self.WIN.blit(counter_surface, (50,30))
        self.board.draw(self.WIN)
        pygame.display.flip()