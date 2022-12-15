import os


def getList(filename):
    fichier = open(filename, 'r')
    listeLignes = []
    for ligne in fichier:
        ligne = ligne.strip()
        listeLignes.append(ligne)
    return listeLignes

# Crée les dossiers d'images de nom situés das filename dans folder
def createDirectories(folder, filename):
    fichier = open(filename, 'r')
    listeLignes = []
    for ligne in fichier:
        ligne = ligne.strip()
        listeLignes.append(ligne)
        try:
            os.makedirs(folder+"/"+ligne)
        except:
            pass
    fichier.close()
    return listeLignes
