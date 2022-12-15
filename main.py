from fct_model.analyse_model import *
from fct_database.database_building_and_update import *
import sqlite3
import keras.models
import numpy as np
from matplotlib import pyplot as plt
import shutil
#Dans le fichier config.py, définir database comme le chemin d'accès à la database, dossier contenant les photos,
#les visages, et les vecteurs de représentation des personnes de "personnes.txt"
from config import database

conn = sqlite3.connect("RVclasse.db")
cur = conn.cursor()

myModel = keras.models.load_model("Modèle VGG")

#########################################
#crée les dossiers de photos d'élèves dans database/photos, lorsque le projet est créé pour la 1ere fois
createDirectories(database+"photos/", "personnes.txt")

# Reset la DB, si besoin 
print("Reset de la DB et des fichiers photos et vecteurs")
resetDB()
try:
    shutil.rmtree(database+'students_photos')
    shutil.rmtree(database+'students_vectors')
    os.mkdir(database+'students_photos')
    os.mkdir(database+'students_vectors')
    os.mkdir(database+'photos')
except:
    pass

print("Création de la DB...")
cur.execute("CREATE TABLE IF NOT EXISTS Student(id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, student_mail TEXT, parent_mail TEXT, photo_visage TEXT, number_faces INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS Faces(photo PRIMARY KEY, student_id INTEGER, FOREIGN KEY (student_id) REFERENCES Student(id))")
conn.commit()
print("DB créée\n")

#Construit la DB à partir d'un dossier de dossiers-étudiants contenant chacun des photos de la personne
buildDatabase3("personnes.txt", database)


######################################

#Affiche la DB
seeDB()
