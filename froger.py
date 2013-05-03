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
	try:
		print ("Liste des sigles :" +str(sigle))
	except NameError:
		print ("Sigles non définis : erreur")

	# On peut maintenant renvoyer la liste des variantes
	return {"sigle":sigle,"variantes":variantes}

def verifier_variantes(analyse):
	"""Vérifier que nos variantes prennent bien en compte tout les manuscrits.
	Si une variante ne prend pas en compte tous les manuscrits le signaler et l'effacer.
	On suppose qu'on a un apparat positif en entré. Cf p. 66"""
	sigles = set(analyse["sigle"])
	variantes = analyse["variantes"]
	
	# parcourir chacun des variantes

	for var in variantes:
		if set(var[0]+var[1]) != sigles:
			print ("Lieu ne prenant pas en compte tous les manuscrits" + str(var))
			variantes.remove(var)
	return {"sigle":analyse["sigle"],"variantes":variantes}

def grouper_variantes(variantes):
	"""Grouper les variantes, en ne conservant que la partie variante : 
	cf tableau p. 69"""
	groupes ={}
	for var in variantes:
		gr = frozenset(var[1])
		try:	#a-t-on déjà eu cette variante?
			groupes[gr] = groupes[gr] + 1
		except:
			groupes[gr] = 1		
	
	return groupes

def __main__():
	import sys
	import getopt
	option = getopt.getopt(sys.argv[1:],'')[1]
	for fichier in option:
		analyse = lecture_fichier(fichier)
		analyse = verifier_variantes(analyse)
		groupes  = grouper_variantes(analyse["variantes"])
		for gr in groupes:
			print (str(gr) + " : " + str(groupes[gr]))
__main__()