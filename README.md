# projMO
Project collaboration between Emmanuel Odeke and Brennen McPhee(Project McPhee Odeke)

Description: 

This implements predictive text program in python. It takes input from the user
in the form of a word and it will display any words that are similar to
the word entered. The program will also display a rating which tells the
user how close to what they typed the suggested word is. If the user wants
they can define a minumum rating that the suggested words must be greater
than.

The program can be used in either a GUI by running gui.py. If the GUI is
used there are two entry boxes, one for the word that is to be checked
and the other is for the minimum rating. Below that there are two lists that
are displayed, one for the suggested words and the other for the rating
that corresponds with the entry next to it.

If the user decides to use the command line then they need to run repl.py
which is in the predict folder. This program can either take input by just
typing the word that they want to check. If the user wishes to set a
minimum rating then it must be in the form of 'wordtocheck 90'. Where 
'wordtocheck' is the word that the user wants to check and '90' is the
minimum rating.
