#!/usr/bin/python
import sys
import os
import logging
import math
import random
import itertools
import Tkinter
import enum
import re
from pprint import pprint

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()

class Direction(enum.Enum):
  clockwise = 1
  anticlockwise = 2

class Pyramind(object):
  
  version = 1.0
  author = 'Ananth Sridhar'
  author_email = 'araghav.s@gmail.com'
  use_gui = False
  # use_gui = True

  def __init__(self, pyramid_base_length=4):
    random_number = lambda: random.Random().randint(0,9)

    self.pyramid_base_length = pyramid_base_length
    self.pyramid = list()
    self.game_over = False

    for level_height, level_length in itertools.izip(range(0, self.pyramid_base_length), range(self.pyramid_base_length, 0, -1)):
      level = list()
      for element_index in range(0, level_length):
        level.append(random_number())
      self.pyramid.append(level)

    if not self.use_gui:
      while not self.game_over:
        self.clear_screen()
        self.welcome()
        self.help()
        self.display_pyramid()
        self.check_game_over()

        if not self.game_over:
          self.cmd = raw_input('Enter command: ')
          self.process_cmd()
    else:
      raise Exception('GUI not developed')

  def process_cmd(self):
    add_cmd_regex = re.compile('^(\d+)\s+(\d+)$')
    add_cmd = add_cmd_regex.findall(self.cmd)

    if self.cmd == 'c':
      self.rotate_pyramid(Direction.clockwise)
    elif self.cmd == 'a':
      self.rotate_pyramid(Direction.anticlockwise)
    elif len(add_cmd) > 0:
      self.add_number_to_row(*add_cmd[0])
    elif self.cmd == 'ananth is awesome':
      self.pyramid = [ [0 for element in level] for level in self.pyramid ]

  def rotate_pyramid(self, direction):
    rotated_pyramid = list()

    for level_height, level_length in itertools.izip(range(0, self.pyramid_base_length), range(self.pyramid_base_length, 0, -1)):
      level = list()
      for element_index in range(0, level_length):
        if direction is Direction.clockwise:
          level.append(self.pyramid[element_index][-level_height-1])
        elif direction is Direction.anticlockwise:
          level.append(self.pyramid[level_length-element_index-1][level_height])
      rotated_pyramid.append(level)

    self.pyramid = rotated_pyramid

  def add_number_to_row(self, row, add_value):
    row = int(row)
    add_value = int(add_value)
    try:
      if row < 1:
        raise IndexError
      self.pyramid[row-1] = [ (element+add_value)%10 for element in self.pyramid[row-1] ]
      pprint(self.pyramid[row-1])
    except IndexError:
      pass

  def debug_display_pyramid(self):
    debug_pyramid = list()
    for level in self.pyramid:
      debug_level_string = ' '.join([str(element) for element in level])
      debug_pyramid.insert(0, debug_level_string)
    debug_pyramid_string = '\n'.join(debug_pyramid)
        
    logger.debug("\n" + debug_pyramid_string)

  def display_pyramid(self):
    char_display_size = 2
    element_formatter = '{0:' + str(char_display_size) + 's}'
    display_gap = element_formatter.format(' ')
    for indent, level in itertools.izip(2*range(self.pyramid_base_length, -1, -1), reversed(self.pyramid)):
      indent_string = ''.join( [display_gap] * indent )
      level_string = display_gap.join([element_formatter.format(str(element)) for element in level])
      print( indent_string + level_string )

  def clear_screen(self):
    os.system('clear')

  def welcome(self):
    print('** ***     ***************** ***     ')
    print('* * *** * ***  PYRAMIND *** * *** * *')
    print('     *** *****************     *** **')
    print('        WELCOME TO PYRAMIND!!        ')
    print('The objective of the game is to make ')
    print(' all the numbers in the pyramid equal')
    print(' to each other')
    print('\n\n')  

  def help(self):
    print('Commands list:')
    print('\ta                  : rotate pyramid anti-clockwise')
    print('\tc                  : rotate pyramid clockwise')
    print('\t<number> <number>  : row number, and number to add to that row')
    print('Note:')
    print('\ta. numbers wrap around when added. e.g. 9+2 = 1 (not 11), 5+8 = 3 (not 13)')
    print('\tb. row numbers start from the bottom. i.e. bottom row = row number 1, and increases going up')
    print('\t   for e.g. try using the command \'1 1\'. the bottom row should be incremented by 1')
    print('\n\n')

  def check_game_over(self):
    self.game_over = True
    # check_element = 0
    check_element = self.pyramid[0][0]
    for level in self.pyramid:
      for element in level:
        if element != check_element:
          self.game_over = False
          return

    print('\n')
    print('O, stunning beautiful mind! I desire thee wisdom!')

def launch_game():
  try:
    logger.info('Launching game')
    pyramind = Pyramind()
  except KeyboardInterrupt:
    print('\n')
    print('Too tough for ya?!!')
    print('Adios, amigo!')

if __name__=='__main__':
  launch_game()
