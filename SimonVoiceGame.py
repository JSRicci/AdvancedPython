"""Welcome to Joe Ricci's Simon Says Game
    In this game you can speak to your computer
    as your input instead of typing or clicking.
    You will see a splash screen with instructions.
    Follow the instructions shown on display to play the game.
    Another option is that you can enable the Debug mode and the game will play itself!
    You can see how the game works and all of the troubleshooting text that appears in the CLI.
    There are two ways you can speak to the program and it will recognize your input.
    1) Say each color in order
    2) Say 'and' in between each color
    As you progress, the patterns get harder.
    the maximum level is 20, once you pass this point you win!
    Good Luck!
    """
"""Note: There is a bug in the system when using debug, sometimes you do not have to click inside the window
in order to continue the process."""
import pygame as pg
import speech_recognition as sr
import time, gtts, sys, os, pyaudio, random,wave
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import speech
import pywin32_system32
from threading import Thread
r = sr.Recognizer()
colorinputpattern = []
debug = True

#Class options contains all the variables used inside the game.
class options:
    # Game Title Window
    TITLE = "Voice Simon Says Game"
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    #Set default level
    LEVEL = 1

    # Set colors
    BGROUND = WHITE

    # Game FPS
    FPS = 30
    # Window Size
    W_WIDTH = 640
    W_HEIGHT = 680

    COUNT = True
    COLORS = ['red', 'blue', 'green', 'yellow']
    COLORPATTERN = []
    MOUSEPATTERN = []
    VOICEPATTERN = []
    W_WIDTH = 640
    W_HEIGHT = 480
    BOX_WIDTH = (W_WIDTH / 2) - 10
    BOX_HEIGHT = (W_HEIGHT / 2) - 15

    score = 0
    BLUESQUARE = pg.Rect(0, 0, BOX_WIDTH, BOX_HEIGHT)
    REDSQUARE = pg.Rect(0, (W_HEIGHT / 2), BOX_WIDTH, BOX_HEIGHT)
    YELLOWSQUARE = pg.Rect(W_WIDTH / 2, 0, BOX_WIDTH + 10, BOX_HEIGHT)
    GREENSQUARE = pg.Rect(W_WIDTH / 2, W_HEIGHT / 2, BOX_WIDTH + 10, BOX_HEIGHT)
    CURRENTSTEP = 0
    WAITINGFORINPUT = False

#Class game contains majority of the code used to run the game.
class game:

    level = 1
    splash = True
    def __init__(self):
        if debug is True:
            print('Running initialization')
        global pattern
        global colorinputpattern
        pg.init()
        self.screen = pg.display.set_mode((options.W_WIDTH, options.W_HEIGHT))
        pg.display.set_caption(options.TITLE)
        if game.splash is True:
            self.splashscreen()
            time.sleep(5)
            game.splash = False
        #Setup the background for the game
        self.background()

        # Draw each square onto background
        self.drawBoxes()

        # Blit everything to the screen
        pg.display.flip()

        self.clock = pg.time.Clock()
        self.running = True

        self.start_game()
    # This function is from the play sound example done in class, modified to be used appropriately in this program
    def playsound(self):
        inputstream = wave.open(
            "C:\\Users\\jricc3\\OneDrive - University of New Haven\\Fall 2016\\Adv Python\\Class 9\\shortbeep.wav")

        pyoutputstream = pyaudio.PyAudio()

        outputstream = pyoutputstream.open(output=True, rate=inputstream.getframerate(),
                                           channels=inputstream.getnchannels(),
                                           format=pyoutputstream.get_format_from_width(inputstream.getsampwidth()))
        chunksize = 1024
        data = inputstream.readframes(chunksize)
        while data != "":
            outputstream.write(data)
            data = inputstream.readframes(chunksize)
        outputstream.stop_stream()
        outputstream.close()
        inputstream.close()
        pyoutputstream.terminate()
        return
    #Create the background for the game
    def background(self):
        # Fill background
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((options.BGROUND))
        self.screen.blit(background, (0, 0))
        self.drawBoxes()
    #Start a new game
    def new(self):
        game.__init__(self)
    #Create a pattern for the user to try and copy
    def setPattern(self, color):
        options.COLORPATTERN.append(color)
        print("Here is the color pattern:" +str(options.COLORPATTERN))
        self.updateBoxes(options.COLORPATTERN)

        pass
    #Draw the boxes on screen
    def drawBoxes(self):
        level = len(options.COLORPATTERN)
        if debug == True:
            print('drawBoxes')
        pg.draw.rect(self.screen, options.BLUE, options.BLUESQUARE, 1)
        pg.draw.rect(self.screen, options.RED, options.REDSQUARE, 1)
        pg.draw.rect(self.screen, options.YELLOW, options.YELLOWSQUARE, 1)
        pg.draw.rect(self.screen, options.GREEN, options.GREENSQUARE, 1)
        myfont = pg.font.SysFont("Comic Sans MS", 14)
        label1 = myfont.render("Level: " + str(level), 1, options.BLACK)
        self.screen.blit(label1, (290, 462))
    #Update the boxes in the game to represent the updated color pattern
    def updateBoxes(self, COLORPATTERN):
        for i in COLORPATTERN:
            thread = Thread(target = game.playsound, args = (10, ))
            if debug == True:
                print("updating boxes")
            if i == 'blue':
                #self.playsound()
                self.background()
                pg.display.update()
                pg.draw.rect(self.screen, options.BLUE, options.BLUESQUARE, 0)
                pg.display.flip()
                time.sleep(1)
                pg.draw.rect(self.screen, options.WHITE, options.BLUESQUARE, 0)
                pg.display.flip()
                self.background()
                thread.start()
            elif i == 'red':
                #self.playsound()
                self.background()
                pg.display.update()
                pg.draw.rect(self.screen, options.RED, options.REDSQUARE, 0)
                pg.display.flip()
                time.sleep(1)
                pg.draw.rect(self.screen, options.WHITE, options.REDSQUARE, 0)
                pg.display.flip()
                self.background()
                thread.start()
            elif i == 'yellow':

                self.background()
                pg.display.update()
                pg.draw.rect(self.screen, options.YELLOW,options.YELLOWSQUARE, 0)
                pg.display.flip()
                time.sleep(1)
                pg.display.update()
                pg.draw.rect(self.screen, options.WHITE, options.YELLOWSQUARE, 0)
                pg.display.flip()
                self.background()
                thread.start()
            elif i == "green":
                #self.playsound()
                self.background()
                pg.display.update()
                pg.draw.rect(self.screen, options.GREEN, options.GREENSQUARE, 0)
                pg.display.flip()
                time.sleep(1)
                pg.draw.rect(self.screen, options.WHITE, options.GREENSQUARE, 0)
                pg.display.flip()
                self.background()
                thread.start()
            time.sleep(1)
            self.background()

    def start_game(self):
        #Let us know that we are in the start game function
        if debug == True:
            print('Game has started')
        global WAITINGFORINPUT
        global CURRENTSTEP
        global clickedButton
        global colorinputpattern
        clickedButton = None
        #randomly pick a color for the options and assign it to color
        color = random.choice(options.COLORS)
        #Wait until the player clicks in the game window and the color pattern has been established
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and options.WAITINGFORINPUT is True:
                #Check to see that the event worked and the waiting for input logic worked
                if debug == True:
                    print('You clicked in the game')
                #check the color input pattern
                colorinputpattern = game.getButtonClicked(self)
                options.WAITINGFORINPUT = False
        #When we are not waiting for user input, append a new color to the color list and set watiing input to true
        if not options.WAITINGFORINPUT:
            if debug == True:
                print('Waiting for input and appending to color list')

            self.setPattern(color)
            options.WAITINGFORINPUT = True
        else:
            #Enter a loop while waiting for the user to click inside the window
            if debug is True:
                print('Waiting for user input')
            else:
                print('')
    def splashscreen(self):
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(options.BLACK)
        # pick a font and set its size
        myfont = pg.font.SysFont("Comic Sans MS", 24)
        # apply it to text on a label
        label1 = myfont.render("Welcome to Joe Ricci's ", 1, options.YELLOW)
        label2= myfont.render("Simon Says Voice Game!", 1 , options.YELLOW)

        # put the label object on the screen at specified point
        self.screen.blit(label1, (210, 150))
        self.screen.blit(label2, (200, 200))
        # Blit everything to the screen
        pg.display.flip()
        time.sleep(5)
        myfont = pg.font.SysFont("Comic Sans MS", 24)
        label1 = myfont.render("Welcome to Joe Ricci's ", 1, options.BLACK)
        label2 = myfont.render("Simon Says Voice Game!", 1, options.BLACK)
        self.screen.blit(label1, (210, 150))
        self.screen.blit(label2, (200, 200))
        pg.display.flip()
        background.fill(options.BLACK)
        instruction = myfont.render('The game will begin shortly', 1 ,options.YELLOW, options.BLACK)
        instruction2 = myfont.render('so in the mean time, here are the instructions:', 1, options.YELLOW, options.BLACK)
        # put the label object on the screen at specified point and write to screen
        self.screen.blit(instruction, (20, 150))
        self.screen.blit(instruction2, (50, 200))
        # Show all items drawn to screen
        pg.display.flip()
        time.sleep(5)
        background.fill(options.BLACK)
        instruction = myfont.render('The game will begin shortly,', 1, options.BLACK, options.BLACK)
        instruction2 = myfont.render('so in the mean time, here are the instructions:', 1, options.BLACK, options.BLACK)
        # put the label object on the screen at specified point
        self.screen.blit(instruction, (20, 150))
        self.screen.blit(instruction2, (50, 200))
        # Blit everything to the screen
        pg.display.flip()
        background.fill(options.BLACK)
        instruction = myfont.render('A colored box will flash', 1, options.YELLOW, options.BLACK)
        instruction2 = myfont.render('When you are ready, click anywhere in the window', 1, options.YELLOW, options.BLACK)
        instruction3 = myfont.render('and say the color that you saw flash.', 1, options.YELLOW, options.BLACK)
        instruction4 = myfont.render('As you progress through the levels,',1 , options.YELLOW, options.BLACK)
        instruction5 = myfont.render('the pattern will get longer.', 1, options.YELLOW, options.BLACK)
        instruction6 = myfont.render('This will continue until you ', 1 ,options.YELLOW, options.BLACK)
        instruction7 = myfont.render('reach level 20 and you win the game!', 1 ,options.YELLOW, options.BLACK)
        # put the label object on the screen at specified point
        self.screen.blit(instruction, (20, 50))
        self.screen.blit(instruction2, (20, 100))
        self.screen.blit(instruction3, (20, 150))
        self.screen.blit(instruction4, (20, 200))
        self.screen.blit(instruction5, (20, 250))
        self.screen.blit(instruction6, (20, 300))
        self.screen.blit(instruction7, (20, 350))
        # Blit everything to the screen
        pg.display.flip()
        time.sleep(10)
    #When the player loses this function is called
    def lose(self):
        quit()
    #When user clicks, it means they are ready to input through microphone and say pattern
    def getButtonClicked(self):
        #The length of the pattern is the same as the level
        level = len(options.COLORPATTERN)
        #To let programmer know that we are in this function
        if debug == True:
            print('getting voice input')

        print('Welcome to level: ' +str(level))
        #Reset voice input to an empty list
        voiceinput = []
        stop = False
        while stop == False:
            try:
                #When debug is set to false, use the microphone as user input
                if debug == False:
                    with sr.Microphone(0) as mic:
                       # mic = speech_recognition.Microphone(0)
                        r.energy_threshold = 3000
                        r.dynamic_energy_threshold = True
                        print('Tell me the pattern')
                        audio = r.listen(mic)
                        text = r.recognize_google(audio)
                        print("You said: ", text)
                #Debug is used to automate level increment logic. Much quicker than using voice.
                elif debug == True:
                    text = options.COLORPATTERN
                    print("You said: ", text)
                # if level is over 20 then the player wins
                if level == 21:
                    print("Game over, you win!")
                #When the user is on level 1, compare the two elements in the seperate lists
                elif level == 1:
                    print('checking the color logic')
                    for i in text:
                        print(i)
                        for c in options.COLORPATTERN:
                            print(c)
                            if i == c:
                                print('we have a match!')
                            else:
                                print('There is not a match')
                                self.lose()
                                break
                            stop = True
                #If the user says and in between each color then sepearate the colors and put into list
                elif 'and' in text and level > 1:
                    voiceinput = text.split('and')
                    voiceinput = text
                    level += 1
                    stop = True
                #If the user does not say and in between colors then use this logic
                elif level > 1 and text == options.COLORPATTERN:
                    print('doing more stuffs')
                    level += 1
                    stop = True
                #Game win logic
                elif level == 21:
                    print('you win!')
            except sr.UnknownValueError as e:
                print(e)
        return voiceinput
#Set the class "game" as "g"
g = game()
#done will stop the game when = False
done = True
#Main game loop, while done == True the game will run
while done == True:
    #Start a new game to initialize the game
    g.new()
    g.start_game()
    #When the user tries to quit, sets done = False and ends game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = False
#quit game
pg.quit()
