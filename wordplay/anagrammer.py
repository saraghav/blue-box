#!/usr/bin/python
import re
from pprint import pprint

class Anagrammer(object):

  version = 1.0
  author = 'Ananth Sridhar'
  author_email = 'araghav.s@gmail.com'

  def __init__(self):
    while True:
      single_word_re = re.compile('^\w+$')
      string = raw_input('Enter word: ')
      if single_word_re.match(string):
        self.string = string
        anagrams = self.find_all_anagrams(self.string)

      self.anagrams = anagrams

      pprint(self.anagrams)
      print('{0} anagrams found'.format(len(self.anagrams)))

  def find_all_anagrams(self, string):
    if len(string) == 1:
      return list(string)

    sub_anagrams = self.find_all_anagrams(string[1:])
    anagrams = list()
    for sub_anagram in sub_anagrams:
      for index in range(0, len(string)):
        new_anagram = sub_anagram[0:index] + string[0] + sub_anagram[index:]
        anagrams.append(new_anagram)
    return anagrams

if __name__=='__main__':
  try:
    anagrammer = Anagrammer()
  except KeyboardInterrupt:
    pass

