#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Auteur : Maïeul ROUQUETTE
# Licence : GPL3 
# https://www.gnu.org/licenses/gpl-3.0.html
# Version 0.1

import default as config

def lecture_ligne(ligne):
	"""Analyser une ligne"""
	
	#Supprimer les commentaires
	comment = ligne.find(config.comment)
	ligne = ligne[:comment]
	return ligne
	    
	
def lecture_fichier(fichier):
        """Lire le fichier, ligne par ligne"""
        fichier = open(fichier,"r")
        for ligne in fichier:
            print(lecture_ligne(ligne))

def __main__():
	import sys
	import getopt
	option = getopt.getopt(sys.argv[1:],'')[1]
	for fichier in option:
		lecture_fichier(fichier)
__main__()