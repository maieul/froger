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
	
	if len(ligne) == 0:
		return (False,False)
	#pour la liste des sigles
	if ligne[0:len(config.sigle)] == config.sigle:
	   sigles = ligne[len(config.sigle):]
	   return config.sigle,sigles.split(config.sep_temoin)
	
	#pour dectecter qu'on passe aux variantes
	elif ligne.find(config.sep_variante):
	    variante = ligne.split(config.sep_variante)
	if len(variante) != 2:
		print ("Lieu n'ayant pas exactement deux variantes : "+ligne)
	else:
		variante[0] = variante[0].split(config.sep_temoin)
		variante[1] = variante[1].split(config.sep_temoin)
		return variante
	
	return (False,False)


	
def lecture_fichier(fichier):
	"""Lire le fichier, ligne par ligne"""
	fichier = open(fichier,"r")
	variantes = []
	for ligne in fichier:
	    analyse =  lecture_ligne(ligne)
	    
	    # trouver les sigles
	    if analyse[0] == (config.sigle):
		    sigle = analyse[1]
		    
	    #trouver les variantes
	    elif analyse != (False,False):
		    variantes.append(analyse)
	if !sigle:
		print "Sigles non définis : erreur"
		break


def __main__():
	import sys
	import getopt
	option = getopt.getopt(sys.argv[1:],'')[1]
	for fichier in option:
		lecture_fichier(fichier)
__main__()