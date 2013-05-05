#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Auteur : Maïeul ROUQUETTE
# Licence : GPL3 
# https://www.gnu.org/licenses/gpl-3.0.html
# Version 0.1.1
#(frozenset({'B', 'C', 'D', 'E', 'F', 'O'}), frozenset({'A', 'B', 'C', 'D', 'E', 'F', 'G', 'O'})) > pas bon
import default as config
from collections import Counter
import networkx as nx
#import matplotlib.pyplot as plt
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

def construire_stemma_manuscrit(groupes,stemma,sigle):
	'''Construit, à partir d'un stemma par ensemble des manuscrits et des groupes classé par niveau un stemma par manuscrits. Cf p. 75. Et p. 78 :
	"1 groupe de manuscrits / 1 manuscrit qui commet des fautes / la collection de fautes commises par lui > trois façon de désigner la même chose"'''
	niveaux = list(groupes.keys())
	niveaux.sort()
	niveaux.reverse()
	stemma_cop = stemma.copy()
	stemma_man = nx.Graph()
	correspondance = {} #tableau permettant d'obtenir la correspondance entre un groupe de manuscrit et le manuscrit auteur de la faute
	
	# d'abord, trouver l'origine
	enfants = frozenset()
	for edge in stemma.edges(sigle):
		enfants = enfants.union(edge[1])
	stemma.remove_node(sigle)	


	correspondance[sigle] = sigle - enfants
	# ensuite, descendendre niveau par niveau
	for n in niveaux:
	 	for gr in groupes[n]:
	 		enfants = frozenset()
	 		for edge in stemma.edges(gr):
	 			enfants = enfants.union(edge[1])
	 		stemma.remove_node(gr)
	 		correspondance[gr] = gr - enfants

	 # maintenant qu'on a les correspondances, on peut établir les liens.
	for edge in stemma_cop.edges():
		stemma_man.add_edge(correspondance[edge[0]],correspondance[edge[1]])
	
	return stemma_man
def construire_stemma_ensemble(sigles,groupes):
	"""Construire le stemma à partir des groupes de manuscrits avec variantes, déjà classé par niveau (taille)"""

	niveaux = list(groupes.keys())
	niveaux.sort()
	#sans doute manière de faire plus simple
	stemma = nx.Graph()
	ensemble_noeud_prec = [] # noter le nœud correspondant à chaque ensemble analysé. Ex : p. 75, le nœud G correspond à l'ensemble {G,A}. 
	#A chaque niveau de l'arbre, on va remplir ce tableau, qu'on consultera au niveau supérieur.
	#Si on relie un nœud à un autre, on supprime le nœud de ce tableau.

	# on commence par le bas de l'arbre, on suppose (pour le moment, qu'on a tjr en bas des groupes de 1 manuscrits)
	for n in niveaux:
		# pour le moment, on ne se préoccupe pas des éventuelles contamination
		for gr in groupes[n]: # tous les groupes du niveau donné
			stemma.add_node(gr)#dans tous les cas on place le noeud
			if n !=min(niveaux):
				# si on est au plus bas dans le nombre de manuscrits, alors on place notre nœud sans le relier à rien. 
				#p. 75 correspond à la ligne "1 manuscrit"
				for noeud in ensemble_noeud_prec.copy(): # on cherche à savoir à quel nœud "inférieur" se rattache notre nœud.
					
					if noeud.issubset(gr): 		  # si on trouve un nœud inférieur
						#d'abord placer l'arc
						
						stemma.add_edge(gr,noeud)

						#ensuite signalé qu'on a déjà rattaché un nœud de l'étage du dessous
						ensemble_noeud_prec.remove(noeud)
						print ("après modif")			# ne pas oublier 
			ensemble_noeud_prec.append(gr)

	# ne pas oublier d'ajouter le niveau ultime, comprenenant tt les manuscrits
	stemma.add_node(sigles)
	for noeud in ensemble_noeud_prec:
		stemma.add_edge(sigles,noeud)
	return stemma
	
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
	return {"sigle":frozenset(sigle),"variantes":variantes}

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
def niveau_groupes(groupes):
	"""Classe les groupes par niveau"""
	tri_groupes = {}
	
	### trier les groupes par taille
	for gr in groupes.keys():
		try:
			tri_groupes[len(gr)] = tri_groupes[len(gr)]+[gr]
		except:
			tri_groupes[len(gr)] = [gr] 
	return tri_groupes
def grouper_variantes(variantes):
	"""Grouper les variantes, en ne conservant que la partie variante : 
	cf tableau p. 69"""
	groupes = Counter()
	for var in variantes:
		gr = frozenset(var[1])
		groupes[gr] += 1
	return groupes

def __main__():
	import sys
	import getopt
	option = getopt.getopt(sys.argv[1:],'')[1]
	for fichier in option:
		analyse = lecture_fichier(fichier)
		analyse = verifier_variantes(analyse)
		groupes = niveau_groupes(grouper_variantes(analyse["variantes"]))
		stemma  = construire_stemma_ensemble(analyse["sigle"],groupes)
		stemma  = construire_stemma_manuscrit(groupes, stemma,analyse["sigle"])
		for edge in stemma.edges():
			print (edge)

__main__()