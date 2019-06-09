from .exceptions import *
from random import choice


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit == True and miss == True:
            raise InvalidGuessAttempt()

        self.letter = letter
        self.hit = hit
        self.miss = miss

    def is_hit(self):
        if self.hit == True:
            return True
        else:
            return False

    def is_miss(self):
        if self.miss == True:
            return True
        else:
            return False

        


class GuessWord(object):
    def __init__(self,answer):
        if answer == '':
            raise InvalidWordException()

        self.answer = answer.lower()
        self.masked = len(self.answer) * '*'
    
    def new_masked(self,character):
        new_mask = ''
        for index,char in enumerate(self.answer):
            #Check masked
            if self.masked[index] != '*':
                new_mask += self.masked[index]
            elif character == char:
                new_mask += character
            else:
                new_mask += '*'
                
        return new_mask



    def perform_attempt(self,character):
        character = character.lower()
        if len(character) > 1:
            raise InvalidGuessedLetterException()
        if character in self.answer:
            self.masked = self.new_masked(character)
            attempt = GuessAttempt(character,hit=True)
            return attempt
        elif character not in self.answer:
            attempt = GuessAttempt(character,miss=True)
            return attempt


class HangmanGame(object):
    #Global WORD_LIST
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self,word_list=None,number_of_guesses=5):
        #Set word list
        if word_list == None:
            word_list = self.WORD_LIST
        #set remaining guesses
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(word_list))
        self.previous_guesses = []

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        else:
            return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        else:
            return False

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        else:
            return False

    def guess(self,letter):
        if self.is_finished():
            raise GameFinishedException()

        
        self.previous_guesses.append(letter.lower())
        attempt = self.word.perform_attempt(letter)
        if attempt.miss == True:
            self.remaining_misses -= 1

        if self.is_won() == True:
            raise GameWonException()
        elif self.is_lost() == True:
            raise GameLostException()
        
        return attempt

    #get random word for word_list
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return choice(word_list)


