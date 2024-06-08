import pandas as pd
# import sys, getopt
import argparse


file = ''
nb_eleves = 0

class Entite:
    
    
    # mariage = "null"
    def __init__(self, nom, places =1, *elements):
        self.nom = nom
        self.preferences = list(elements)
        self.mariage = []
        self.places = places
        self.liste_pretendant = []
        self.list_souhait = []
        self.increment_rejet = 0
    
    def __str__(self) -> str:
        string = "Nom=" + self.nom
        string += " Pref=" + str(self.preferences)
        string += " Places=" + str(self.places)
        return string

    def __repr__(self):
        return self.__str__() + "\n"

    def getList(self):
        return self.preferences

    def getNom(self):
        return self.nom    



def verifMariage(ecoles):
    total_places = 0
    total_places_temp = 0

    for ecole in ecoles:
        total_places += ecole.places
        total_places_temp += len(ecole.mariage)

    if total_places ==  total_places_temp:
        return False
    return True

def stable_mariage_alban(eleves, ecoles):
    
    pasfini = True
    dico_balcon = {}
    i=0
    
    #creation d'une liste de souhait pour si on veut épouser plusieurs femmes
    for eleve in eleves:
        for nbchoix in range(eleve.places):
            eleve.list_souhait.append(eleve.getList()[nbchoix])
  
    #correspondre choix aux courtisans
    for eleve in eleves:
            dico_balcon[eleve] = eleve.list_souhait  # plus une valeur mais une liste de valeur pour quand on inverse ecole et eleve dans l'algo

    while pasfini:
        i += 1 #represente les tours
        for ecole in ecoles:
            #condition pour sortir de la boucle 
            pasfini = verifMariage(ecoles)

            for cle, valeurs in dico_balcon.items():
                if ecole.getNom() in valeurs and cle not in ecole.liste_pretendant:
                    ecole.liste_pretendant.append(cle)      
            
            #Si L'ECOLE A UN PRETENDANT AU MOINS
            if len(ecole.liste_pretendant) > 0:    
                
                #trier la ligne avec les preferences des femmes
                ecole.liste_pretendant.sort(key=lambda x: ecole.preferences.index(x.getNom()))

                ecole.mariage.clear()#on vide la liste pour pas avoir de doublons

                if len(ecole.liste_pretendant) <= ecole.places:
                    ecole.mariage.extend(ecole.liste_pretendant)
                else:
                    ecole.mariage.extend(ecole.liste_pretendant[:ecole.places])
                  
                list_pret_temp = ecole.liste_pretendant.copy()
                 
                for rejete in list_pret_temp:
                    if rejete not in ecole.mariage:
                        ecole.liste_pretendant.remove(rejete)
                        rejete.list_souhait.remove(ecole.getNom())
                        rejete.list_souhait.append(rejete.getList()[rejete.places + rejete.increment_rejet])
                        rejete.increment_rejet = rejete.increment_rejet + 1  
    
    print("EN " + str(i) + " TOURS")
    for cle, valeur in dico_balcon.items():
        print(f"{cle.getNom()}: {valeur}")           


def import_from_csv(df, places):
    csv = []
    nom = ""
    entite = []
    for i in range(len(df.columns)):
        nom = df.columns[i]
        entite.append(Entite(nom, places))
        for j in range(len(df[nom])):
            entite[i].getList().append(df[nom][j])
    
        csv.append(entite[i])

    return csv

def importFromCsv(df, nb_eleves):
    donnee_extraite = {
        "eleves": [],
        "ecoles": []
    }
    nom = ""
    entites = []

    for i in range(len(df.columns)):
        nom = df.columns[i]
        entites.append(Entite(nom, int(df[nom][0])))
        df_nom_dropna = df[nom].dropna()
        for j in range(1, len(df_nom_dropna)):
            entites[i].getList().append(df_nom_dropna[j])

        if i < nb_eleves:
            donnee_extraite["eleves"].append(entites[i])
        else:
            donnee_extraite["ecoles"].append(entites[i])

    return donnee_extraite


if __name__ == "__main__":
    pd.options.display.max_rows = 9999

    # arg = main(sys.argv)

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-n", "--nb_eleves", type=int, help="nombre d'eleves", required=True)
    argParser.add_argument("-f", "--file", help="csv file", required=True)
    args = argParser.parse_args()

    df = pd.read_csv(args.file)

    data = importFromCsv(df=df, nb_eleves=args.nb_eleves)

    stable_mariage_alban(data["eleves"], data["ecoles"])
