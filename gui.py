#!/usr/bin/env python3

import time

from tkinter import (
	Tk, W, Entry,
	Label, Button,
	Frame, END, Listbox,
)

import os

from predict import utils, constants

IgnoreShortTimeDeltas = False

class Application(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

		self.__index_cache 			= {}
		self.__memoized_matches 	= {}
		self.__last_used_fuzziness 	= -1
		self.__index_path  = os.path.join('predict', constants.DEFAULT_DICT_FILE)

		self.__prev_entry = ''
		self.__prev_tick = self.__cur_tick = 0

		# Rev it up.
		self.load_index(self.__index_path)

	def createWidgets(self):
		"""
		Creates the various widgets for the gui.
		"""
		
		# label for Enter Word
		self.intruction = Label(self, text = "Enter word.")
		self.intruction.grid(row = 0, column = 0, columnspan = 2, sticky = W)

		# label for Suggested Words
		self.title_list = Label(self, text = "Suggested Words:")
		self.title_list.grid(row = 3, column = 0, columnspan = 2, sticky = W)

		# label for Similarity
		self.title_rating = Label(self, text = "Similarity:")
		self.title_rating.grid(row = 3, column = 1, columnspan = 2, sticky = W)

		# entry box
		self.entry = Entry(self)
		self.entry.bind('<Key>', self.on_entry_change)
		self.entry.bind('<KeyRelease>', self.on_entry_change)
		self.entry.grid(row = 1, column = 0, columnspan = 2, sticky = W)

		# list for similar words
		self.similar_list = Listbox(self, width = 15, height = 15)
		self.similar_list.grid(row = 4, column = 0, sticky = W)

		# list for ratings of words
		self.similar_rating = Listbox(self, width = 8, height = 15)
		self.similar_rating.grid(row = 4, column = 1, sticky = W)
		# label for the no matches error
		self.no_match = Label(self, text = 'No matches.')
		self.clear_no_matches()

	def load_index(self, index_path):
		mem_index = self.__index_cache.get(index_path, None)
		if not mem_index:
			mem_index = utils.read_and_index(index_path)
			self.__index_cache[index_path] = mem_index

		return mem_index
	
	def no_matches(self):
		"""
		If there are no matches it will display an error
		"""
		self.no_match.grid(row = 2, column = 1, sticky = W)
	
	def clear_no_matches(self):
		"""
		If there are matches it clears the error message if there was one
		previously.
		"""
		self.no_match.grid_remove()

	def on_entry_change(self, event):
		"""
		When the submit button is pressed the lists clear
	    themselves in preparation for new predicted words. 
		"""
		new_entry = self.entry.get()

		'''
		if IgnoreShortTimeDeltas:
			self.__prev_tick = self.__cur_tick
			self.__cur_tick  = time.clock()

			time_delta = self.__cur_tick - self.__prev_tick

			print('time_delta', time_delta, self.__prev_tick, self.__cur_tick)
			if time_delta < 0.04: # TODO: Determine a good difference

				if len(self.__prev_entry) >= len(new_entry): # Backspace not hit
					self.__prev_entry = new_entry
					return

			self.__prev_entry = new_entry
		'''
	
	    # Gets rid of the error message if it is on the screen
		self.clear_no_matches()

		suggestions = self.get_matches(new_entry)
	
		# function call to get the list of suggested words and ratings
		# display the similar words using
		if not any(suggestions):
			# If there are no matches display an error
			return self.no_matches()

		# deletes current entries in the lists
		self.similar_list.delete(0, END)
		self.similar_rating.delete(0, END)
				
		for rating, suggestion in suggestions:
			self.similar_list.insert(END, suggestion)
			self.similar_rating.insert(END, rating)
	
	def get_matches(self, query, fuzziness=0.65):
		if fuzziness == self.__last_used_fuzziness:
			mem_matches = self.__memoized_matches.get(query, None)
			if mem_matches:
				# print('Memoized hit for ', query)
				return mem_matches
		else:
			# Cache clean out
			print('Cache cleaned out!')
			self.__memoized_matches = {}

		mem_matches = utils.find_matches(query, fuzziness, self.load_index(self.__index_path))
		self.__last_used_fuzziness = fuzziness

		self.__memoized_matches[query] = mem_matches
		return mem_matches
	
def main():
	root = Tk()
	app = Application(master=root)
	app.mainloop()

if __name__ == '__main__':
	main()
