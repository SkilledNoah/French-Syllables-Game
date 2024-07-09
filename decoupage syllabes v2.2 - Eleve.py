from tkinter import *   # interface graphique, valeurs booleennes (TRUE,FALSE)
from tkinter.messagebox import *    # boîte de dialogue
from random import randint

# ---------------------------

def charger_dico(source): # recopie le contenu du fichier source dans la liste listedico
    
    fs = open(source,'r')
    liste_dico=[]

    while 1:
        txt = fs.readline()
        long=len(txt)
        if txt =='':
            break
        txt=txt[0:long-1]
        liste_dico.append(txt)
   
    fs.close()

    return liste_dico

# ---------------------------


def est_voyelle (lettre):

    r=FALSE
    global lVoyelle          # variable globale 

    for v in lVoyelle:       # v prend chaque élément de la liste
        if lettre == v:
            r=TRUE
            break

    return r

# ---------------------------

def est_consonne (lettre):

    r=FALSE
    global lConsonne

    for c in lConsonne:        # c prend chaque élément de la liste
        if lettre == c:
            r=TRUE
            break

    return r

# ---------------------------

def enregistre_syllabe (debut,fin):

    lTemp=""    #chaine vide (syllabe)
    global lSyllabe
    
#    print("debut;",debut,"fin:",fin)
    
    for k in range (debut,fin+1): # ajout lettres de la syllabe dans lTemp
        lTemp=lTemp+mot[k]

    lSyllabe.append(lTemp)  # on rajoute la syllabe dans la liste

#    print("syllabes: ",lSyllabe)
    
    return

# ---------------------------

def randomcut():
    
    global lSyllabe
    global listeTemp, listeFin # variables globales car fonction recursive
    
    for n in range(len(lSyllabe)):  # index de la liste
        listeTemp.append(lSyllabe[n])
 
    for i in lSyllabe:  # élements de la liste
        x=randint(0,len(listeTemp)-1)  # prend un entier entre 0 et longueur liste -1 (-1 car liste commence a 0)
        listeFin.append(listeTemp[x])
        del(listeTemp[x])  # pour eviter 2x la même syllabe
        
    if listeFin[0]==lSyllabe[0]:
              
        listeTemp=[]
        listeFin=[]
   
        randomcut()                 #fonction recursive (rappelée par elle-même) 

    return

# ---------------------------

def decoupe():

    global lVoyelle, lConsonne, lSyllabe, listeTemp, listeFin, liste_mots, mot

    lSyllabe=[]
    listeTemp=[]
    listeFin=[]

    lm=len(mot)
    i=0
    while(i<lm):


# test: ou-ragan, ouz-bekistan, our-sin, a-bricot, ar-tiste, ar-river


        if est_voyelle(mot[i]):
            j=i+1
        
            while (j < lm):             # plusieurs voyelles à la suite
                if est_voyelle(mot[j]):
                    j=j+1                
                else:
                    break

            if j < lm and j+1 < lm :
                if est_consonne(mot[j]) and est_consonne(mot[j+1]):  # 2 consonnes qui se suivent

                    s=mot[j]+mot[j+1] # 2 lettres à tester pour cas specifique ex: st
                
                    if (mot[j+1] in ('r','t','h')) and (mot[j] != mot[j+1]) and s not in ("rt","xt","nt"):
                    # cas 2ème consonne = r ; a-bricot, a-sterisque, a-chete etc excepté ar-river, ar-tiste (!=r)
                        j=j-1

                else:
                    j=j-1 # 1 seule consonne

            enregistre_syllabe(i,j)

            i=j+1 # debut syllabe suivante
        

#test: ce-ri-se, cro-co-di-le, bou-ton, man-darine, 

        if est_consonne(mot[i]):        
            j=i+1
        
            while (j < lm):             # plusieurs consonnes à la suite
                if est_consonne(mot[j]):
                    j=j+1                
                else:
                    break

            while (j < lm):             # plusieurs voyelles à la suite
                if est_voyelle(mot[j]):
                    j=j+1                
                else:
                    j=j-1
                    break

#        print("AVANT CONSONNES i j lm", i,j,lm)

#        j=j+1

            while (j < lm):             # plusieurs consonnes à la fin de la (dernire) syllabe

#            print("WHILE j:",j)
            
                if j+1 < lm:
                    if est_consonne(mot[j+1]):
                        j=j+1
                        if j+1<lm:

#                        print("i j",i,j)

                            s=mot[j]+mot[j+1] # 2 lettres à tester pour cas specifique ex: nh, lh
                        
                            if (mot[j+1] in ('r','h','l','n','t')) and (mot[j] != mot[j+1]) and s not in ("nh","lh","nt","pt","ct","rt","lt","nt","rn"):
                            #cas particulier ex: ti-Gre, bou-Che, bon-Heur, arti-Ste, lente-ment

#                            print("mot[j+1]",mot[j+1])
                            
                                j=j-1
                                break

                    else:
                        j=j-1     # ne pas prendre la consonne de la syllabe suivante ex: bou-Ton
                        break
                else:
                    break

 #       print("APRES CONSONNES i j lm", i,j,lm)


            
            if j >= lm: #fin du mot
                j=lm-1

            enregistre_syllabe(i,j)


            i=j+1 # debut syllabe suivante

    # decoupage aleatoire (pour mots de plus d'une syllabe)
    if(len(lSyllabe) > 1):
        randomcut()

    return

# ---------------------------

def clavier (event):

    touche = event.keysym   

    # touche Enter
    if touche == 'Return':
        valider()
        
    return

# ---------------------------

def rejouer():

    global liste_mots, mot, listeFin, lSyllabe, niveau

    mot_saisi.set('')

    lSyllabe=[]

    if niveau == 1:
    
        while len(lSyllabe) < 2 or len(lSyllabe) > 3:

#            mot=(input("Choisir le mot à trouver : "))

            position = randint(0,len(liste_mots)-1)
            mot = liste_mots[position]

            print("Mot:",mot)
            decoupe()

    elif niveau == 2:

        while len(lSyllabe) < 4 or len(lSyllabe) > 5:

#            mot=(input("Choisir le mot à trouver : "))

            position = randint(0,len(liste_mots)-1)
            mot = liste_mots[position]

            print("Mot:",mot)
            decoupe()

# affichage du mot decoupé
    label_mot["text"]=listeFin

    print("Syllabes : ",listeFin)

    return

# ---------------------------

def valider ():

    global mot

    if mot_saisi.get() == mot:        
        # le mot est correct : on affiche une boîte de dialogue puis on ferme la fenêtre
        showinfo('Résultat','Mot correct !')
        rejouer()

    else:
        # le mot est incorrect : on affiche une boîte de dialogue
        showwarning('Résultat','Mot incorrect.\nVeuillez recommencer !')
        effacer()

    return

# ---------------------------

def effacer():

    mot_saisi.set('')

    return

# -----------------------------

def niveau1():

    global niveau
    niveau=1
    return

# -----------------------------

def niveau2():

    global niveau
    niveau=2
    return

# -----------------------------

# Création de la fenêtre principale
ma_fenetre = Tk()
ma_fenetre.title('Projet ISN')

#menu niveau de jeu
niveau=1
menu_barre = Menu(ma_fenetre)
menu_niveau = Menu(menu_barre,tearoff=0)
menu_niveau.add_checkbutton(label="Facile - 2-3 syllabes", onvalue=1, offvalue=True, variable=niveau, command=niveau1)
menu_niveau.add_checkbutton(label="Difficile - 4-5 syllabes", onvalue=2, offvalue=False, variable=niveau, command=niveau2)
menu_barre.add_cascade(label="Niveau de jeu", menu=menu_niveau)
ma_fenetre.config(menu=menu_barre)

# variables
lVoyelle=["a","e","i","o","u","y","œ","à","'"]
lConsonne=["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","z","ç","-"]
lSyllabe=[] #liste des syllabes du mot
listeTemp=[] # liste pour découpe aléatoire
listeFin=[] # liste pour découpe aléatoire

# variables interface
mot_saisi = StringVar()
mot_saisi.set('')

# Création d'un widget Label (texte 'SYLLABES')
label_titre = Label(ma_fenetre, text = 'SYLLABES', fg = 'blue')
label_titre.pack(padx = 10, pady = 10)

# Création d'un widget Label (jeu)
label_jeu = Label(ma_fenetre, text = "Recomposez le mot avec les syllabes présentées en désordre", fg = 'black')
label_jeu.pack(padx = 20, pady = 20)

# Création d'un widget Texte
label_mot = Label(ma_fenetre, text = '', fg = 'red', font=20)
label_mot.pack(side = LEFT, padx = 10, pady = 10)

# Création d'un widget Entry (champ de saisie)
champ = Entry(ma_fenetre, textvariable=mot_saisi, bg ='bisque', fg='maroon')
champ.focus_set()
champ.pack(side = LEFT, padx = 10, pady = 10)

# gestion de la touchée Entree
champ.bind('<Key>',clavier)

# Création d'un widget Button (bouton Valider)
bouton_valider = Button(ma_fenetre, text = 'Valider', command = valider)
bouton_valider.pack(side = LEFT, padx = 10, pady = 10)    # Affichage du bouton

# Création d'un widget Button (bouton Jouer)
bouton_jouer = Button(ma_fenetre, text = 'Rejouer', command = rejouer)
bouton_jouer.pack(side = LEFT, padx = 10, pady = 10)    # Affichage du bouton

# Création d'un widget Button (bouton Quitter)
bouton_quitter = Button(ma_fenetre, text = 'Quitter', command = ma_fenetre.destroy)
bouton_quitter.pack(side = LEFT, padx = 10, pady = 10)

# Charge le dictionnaire dans liste_mots
liste_mots=charger_dico('dictionnaire-complet.txt')

# jouer !
rejouer()

# Lancement du gestionnaire d'événements
ma_fenetre.mainloop()

#---------------------              

