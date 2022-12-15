import sqlite3


def get_student_data(id):
    conn = sqlite3.connect("RVclasse.db")
    cursor = conn.cursor()

    stud_data = None
    # Obtient les données de la table Student
    try:
        cursor.execute('SELECT * FROM Student WHERE id=?', (id,))
        stud_data = cursor.fetchone()
    except sqlite3.Error as error:
        print(error)
        return None
    # Si on ne trouve pas d'élèves on renvoie un tuple vide
    if stud_data is None:
        return ()
    # (Nom, prénom, adresses mail parents)
    return (stud_data[1], stud_data[2], stud_data[4])


def get_student_id(nom, prenom):
    conn = sqlite3.connect("RVclasse.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT id FROM Student WHERE nom=? AND prenom=?', (nom, prenom))
        stud_id = cursor.fetchone()
    except sqlite3.Error as error:
        print(error)

    try:
        return stud_id[0]
    except:
        return None