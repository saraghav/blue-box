#!/usr/bin/python
import re
import sys
import logging
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class CrosswordCreator(object):
  version = 1.0
  author = 'Ananth Sridhar'
  author_email = 'araghav.s@gmail.com'

  def __init__(self, input_file):
    self.input_file = input_file
    self.words = list()

    single_word_re = re.compile('^\w+$')

    with open(input_file, 'r') as f:
      for line in f:
        word = line.rstrip()
        word = word.lower()
        if single_word_re.match(word):
          self.words.append(word)

    logger.info('{0} words read'.format(len(self.words)))

    self.find_alphabet_links()
    self.display_alphabet_links()

  def find_alphabet_links(self):
    alphabets = string.ascii_lowercase
    self.alphabet_links = dict((alphabet, list()) for alphabet in alphabets)

    for word in self.words:
      index = self.words.index(word)
      for letter in word:
        if index not in self.alphabet_links[letter]:
          self.alphabet_links[letter].append(index)

  def display_alphabet_links(self):
    for alphabet, word_indices in self.alphabet_links.iteritems():
      print('alphabet = {0}'.format(alphabet))
      for index in word_indices:
        print('\t{0}'.format(self.words[index]))

if __name__=='__main__':
  try:
    crossword_creator = CrosswordCreator(sys.argv[1])
  except KeyboardInterrupt:
    pass
  except IndexError:
    print('ERROR: Please provide a file with a list of words')

