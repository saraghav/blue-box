#!/usr/bin/python
import sys
import os
import logging
import math
import random
import itertools

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()

class Pyramind(object):
  
  version = 1.0
  author = 'Ananth Sridhar'
  author_email = 'araghav.s@gmail.com'

  def __init__(self, pyramid_base_length=4):
    random_number = lambda: random.Random().randint(0,9)

    self.pyramid_base_length = pyramid_base_length
    self.pyramid = list()

    for level_height, level_length in itertools.izip(range(0, pyramid_base_length), range(pyramid_base_length, 0, -1)):
      level = list()
      for element_index in range(0, level_length):
        level.append(random_number())
      self.pyramid.append(level)

    while True:
      self.clear_screen()
      self.display_pyramid()
      a = raw_input('Enter command: ')
      

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
    for indent, level in itertools.izip(range(int(self.pyramid_base_length+1)/2, -1, -1), reversed(self.pyramid)):
      indent_string = ''.join( [display_gap] * indent )
      level_string = display_gap.join([element_formatter.format(str(element)) for element in level])
      print( indent_string + level_string )

  def clear_screen(self):
    os.system('clear')
      

def launch_game():
  logger.info('Launching game')
  pyramind = Pyramind()

if __name__=='__main__':
  launch_game()
