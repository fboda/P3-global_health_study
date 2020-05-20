#!/usr/bin/env python
# coding: utf-8

# -----------------------------------
#     ENVIRONNEMENT - IMPORTS, etc...
# -----------------------------------
# -*- coding: utf8 -*-

import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format   # Nombres avec sepa milliers "," et 2décimales après "."
pd.options.mode.use_inf_as_na = True
import seaborn as sns
from IPython.display import display, Markdown, HTML  # pour gérer un affichage plus joli que la fonction "print"

import time   # Librairie temps pour calculs durée par exemple
trt_start_time = time.time()

# Pour executer des requetes SQL de verification sur des DF
from pandasql import sqldf
execsql = lambda q: sqldf(q, globals())   
# req1 = ''' Select zone1, zone2 From DataFrame Where zone3=xx and zone4='xx' limit 3;'''
# df1 = execsql(req1)
# df1


# #####   <font color='#013ADF'>REPERTOIRE DE TRAVAIL :</font> (du Projet)
# Par defaut on utilisera celui dans lequel se trouve ce fichier jupyter
# %cd D:/DATA_ANALYST/WORK/PJ3


# #####   <font color='#013ADF'>CHARGEMENT DES TABLES de la FAO :</font> dans des Dataframes "Pandas"

# In[4]:


ani = pd.read_csv("DATA/PJ3-Bilan_Alim_Animaux.csv")
veg = pd.read_csv("DATA/PJ3-Bilan_Alim_Vegetaux.csv")
pop = pd.read_csv("DATA/PJ3-Population_par_Pays.csv")
ssn = pd.read_csv("DATA/PJ3-Sous_Alimentation_par_Pays(2013-2016).csv")
cer = pd.read_csv("DATA/PJ3-Produits_Cerealiers_par_Pays.csv")


# #####   <font color='#013ADF'>MISE EN FORME DES DATAFRAMES POUR LE PROJET - </font>  Colonnes : nouveaux noms, suppression colonnes inutiles

# * <font color='#0000FF'><u><strong>pop</strong>  - Population 2013, par Pays (en milliers de personnes)</u>

# In[5]:


pop.columns = ["xx1", "xx2", "CPAYS", "PAYS", "xx3", "xx4", "xx5", "xx6", "xx7", 
               "ANNEE", "UNIT", "VALP", "xx8", "xx9"]
pop.drop(columns=['xx1', 'xx2', 'xx3', 'xx4', 'xx5', 'xx6', 'xx7', 'xx8', 'xx9'], inplace=True)
pop.head()


# * <font color='#0000FF'><u><strong>ani</strong> - Bilan Alimentaire 2013 - Catégorie "Animaux"</u>

# In[6]:


ani.columns = ["xx", "xx", "CPAYS", "PAYS", "CELEM", "ELEMENT", "CPROD", "PROD", "xx", 
               "ANNEE", "UNIT", "VAL", "xx", "xx"]
ani.drop(columns=['xx'], inplace=True)
ani.head(2)


# * <font color='#0000FF'><u><strong>veg</strong> - Bilan Alimentaire 2013 - Catégorie "Végétaux"</u>

# In[7]:


veg.columns = ["xx", "xx", "CPAYS", "PAYS", "CELEM", "ELEMENT", "CPROD", "PROD", "xx", 
               "ANNEE", "UNIT", "VAL", "xx", "xx"]
veg.drop(columns=['xx'], inplace=True)
veg.head(2)


# * <font color='#0000FF'><u><strong>ssn</strong> - Data Sécurité Alimentaire 2013/2016</u></font> (Nb de personnes en sous-nutrition par pays)

# In[8]:


ssn.columns = ["xx", "xx", "CZONE", "ZONE", "CELEM", "ELEMENT", "CPROD", "PROD", "xx", 
               "ANNEE", "UNIT", "VAL", "xx", "xx"]
ssn.drop(columns=['xx'], inplace=True)
ssn.head(2)


# * <font color='#0000FF'><u><strong>cer</strong> - Bilan Alimentaire 2013 - Spécifique "Cérèales"</u>

# In[9]:


cer.columns = ["xx", "xx", "CPAYS", "PAYS", "CELEM", "ELEMENT", "CPROD", "PROD", "xx", 
               "ANNEE", "UNIT", "VAL", "xx", "xx"]
cer.drop(columns=['xx'], inplace=True)
cer.head(2)


# #####   <font color='#013ADF'>DEFINITION DE VARIABLES DE TRAVAIL :</font> (du Projet)

# In[10]:


varcp_chine = 351   # Variable code pays de la chine


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 1</u></font> : Population Mondiale - Année 2013
# - Calcul du nombre total d’humains sur la planète.

# In[11]:


parm1 = "La Population mondiale pour l'année 2013 est :"
parm2 = '{:15,.0f}'.format(pop['VALP'].sum()*1000)
Markdown('<strong>{}</strong><br/>{}'.format(parm1, parm2))


# Le résultat semble un peu élevé. En effet, après étude, on s'aperçoit qu'il y a plusieurs lignes pour la chine.
# Il faudra donc éliminer soit la ligne "Total" avec code pays = 351, soit les 4 lignes details dont les codes pays sont (41,96,128,214)

# In[12]:


pop[pop['PAYS'].str.contains("Chin")]                # Methode avec un "like SQL" sur chaine de caractère
# pop[pop['CPAYS'].isin([41, 96, 128, 214, 351])]    # Methode avec test du CPAYS


# Suppression de la ligne pour le code pays 351.  Maj de la quantité par x1000. Suppression de la colonne unité

# In[13]:


pop.drop(columns=['UNIT'], inplace=True)
pop.drop(pop[pop.CPAYS == varcp_chine].index, inplace=True)
pop['VALP'] *= 1000


# In[14]:


pop_monde = pop['VALP'].sum()  # On stocke cette valeur dans une variable pour réutilisation future
Markdown('<strong>{}</strong><br/>{}'.format(parm1, '{:15,.0f}'.format(pop_monde)))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 2</u></font> : Identifiez des redondances dans les Datas FAO
#     Illustration avec l'exemple du blé en France (a partir du Dataframe "veg")

# In[15]:


veg[(veg['CPAYS'] == 68) & (veg['CPROD'] == 2511)].head(20)


# Effectivement, il y a des données redondantes. On peut définir par exemple, les formules suivantes :
# 
# * [Production] + [Importations Quantite] + [Variation de Stock] **=** <font color='#21610B'>[Disponibilite interieure]</font> + [Exportations Quantite] 
# 
# * <font color='#21610B'>[Disponibilite interieure]</font> **=** [Aliments pour animaux] + [Semences] + [Pertes] + [Traitement] + [Autres Utilisations] + [Nourriture]
# 

# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 3</u></font> : Calculs de Disponibilité Alimentaire  (par Pays/Produit)
#     
#     Exprimée en kcal, puis en Kg de protéines

# #####   <font color='#61210B'>Regroupement des Dataframes "ani" et "veg"</font>  - Ajout de la population (issu du DF pop) et de l"origine" dans un nouveau DF généré : "gen"

# In[16]:


ani["ORIG"] = "animal"
veg["ORIG"] = "vegetal"
temp = ani.append(veg)
temp.head()


# #####   <font color='#61210B'>Affichage des valeurs uniques de la colonne ELEMENT</font>  => Noms des futures colonnes que va générer le "pivot" à l'instruction suivante
# Attention au TRI par Code Element : Il déterminera l'ordre de nos futures colonnes car on gardera l'ordre de tri dans le pivot

# In[17]:


req1 = '''Select Distinct CELEM, ELEMENT From temp 
Order by CELEM limit 20;'''
execsql(req1)


# #####   <font color='#61210B'>Pivot sur le dataframeT</font>  => Les "valeurs" de la colonne élément "pivotent" , pouur devenir des colonnes uniques

# In[18]:


data = temp.pivot_table(
    index=["CPAYS","PAYS","CPROD","PROD","ANNEE","ORIG"],
    columns = ["CELEM", "ELEMENT", "UNIT"], values=["VAL"], aggfunc=sum)
data.columns = ['QT_DISPALI_KG', 'QT_DISPALI_KCAL', 'QT_DISPROT', 'QT_DISPMG', 'QT_VARSTOCK', 'QT_PERTES',
                'QT_TRANSF', 'QT_NOURRIT', 'QT_AUTRES', 'QT_DISPINT', 'QT_PRODUCT', 'QT_ALIMANI', 
                'QT_SEMENCES', 'QT_IMPORT', 'QT_EXPORT']
data = data.reset_index()


# #####   <font color='#61210B'>Jointure avec Df population pour ajout de la colonne VALP</font>  => Nouveau DF finalisé = gen
# 
# Particularité : la jointure avec le Dataframe pop permet d'exclure les données redondantes de la chine (code pays = 351)

# In[19]:


gen = pd.merge(pop, data, how="left")
gen.head()


# #####   <font color='#61210B'>Reséquencement Arbitraire des Colonnes du Dataframe

# In[20]:


cols =  ['ANNEE', 'CPAYS', 'PAYS', 'VALP', 'CPROD', 'PROD', 'ORIG',
            'QT_DISPALI_KG', 'QT_DISPALI_KCAL', 'QT_DISPROT', 'QT_DISPMG',
            'QT_PRODUCT', 'QT_IMPORT', 'QT_VARSTOCK', 'QT_EXPORT', 'QT_DISPINT', 
            'QT_ALIMANI', 'QT_SEMENCES', 'QT_PERTES', 'QT_TRANSF', 'QT_AUTRES', 'QT_NOURRIT']
gen = gen[cols]
gen.head()


# #####   <font color='#61210B'> CALCULS de la disponibilité Alimentaire </font> par Pays/Produit
# en Millions Kcal                     -->  Disp_Alim_Gen = (Dispo_Alimentaire) * (Population) *365 / 1'000'000  
# en Mega Tonnes de proteines   -->  Disp_Alim_Pro = (Dispo_Alim_Proteine) * (Population) *365 * 1000 / 1'000'000'000

# In[21]:


q3 = gen.copy()
q3sel = ['CPAYS', 'PAYS', 'VALP', 'CPROD', 'PROD', 'QT_DISPALI_KCAL', 'QT_DISPROT']
q3['D_Alim_Annu(Mkcal)']= q3['QT_DISPALI_KCAL']*q3['VALP']*365/1000000
q3['D_Alim_Pro_Annu(Mt)']= q3['QT_DISPROT']*q3['VALP']*365*1000/1000000000
q3[q3['CPAYS']==1][q3sel + ['D_Alim_Annu(Mkcal)', 'D_Alim_Pro_Annu(Mt)']].head()


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 4</u></font> : Calculs Ratio et Pourcentage :
# * Calcul Ratio "Energie/Poids" exprimé (en kcal/kg) par Produit
# * Calcul pourcentage de protéines de chaque produit par Pays / Produit  
#   
# Pour le ratio il faut exprimer la Qté de dispo alimentaire en kcal par an et la comparer à la Qté de dispo alimentaire kg.  
# Faire un regroupement par PRODUIT :  
# **Formule** : [RATIO(kcal/kg)] = [QT_DISPALI_KCAL] *365 / [QT_DISPALI_KG]

# #####   <font color='#61210B'>Selection de Zones pour réaffichage, regroupement et calcul

# In[22]:


q4sel = ['CPROD', 'PROD', 'QT_DISPALI_KCAL', 'QT_DISPALI_KG'] 


# In[23]:


q4r = gen.groupby(['CPROD', 'PROD']).sum().reset_index()
q4r.head()


# In[24]:


q4r['RATIO(kcal/kg)']= q4r['QT_DISPALI_KCAL']*365/q4r['QT_DISPALI_KG']
q4r[q4sel + ['RATIO(kcal/kg)']].head()


# #####   <font color='#21610B'> /// Contrôle résultat : Cas de l'Oeuf /// </font> La valeur Wikipedia etant : 147 kcal / 100gr
# Ici je selectionne dans mon dataframe, les lignes dont le nom du produits est "oeufs" et je n'affiche que les colonnes de ma selection q4sel + le ratio

# In[25]:


q4r[q4r['PROD'] == "Oeufs"][q4sel + ['RATIO(kcal/kg)']].head()


# #####   <font color='#61210B'>Pour le pourcentage, on passe tout en grammes/an par exemple</font>
# Faire un regroupement par PAYS / PRODUIT  
# **Formule** : [Taux_Prot(%)] = ( [DISP_PROT] * 365 * 100 ) / ( [Poids(kg)]*1000 )

# In[26]:


q4t = gen.groupby(['CPROD', 'PROD', 'CPAYS', 'PAYS']).sum().reset_index()
q4t['Taux_Prot(%)'] = (q4t['QT_DISPROT']*365*100)/(q4t['QT_DISPALI_KG']*1000)
q4t[['CPAYS', 'PAYS'] + q4sel + ['QT_DISPROT', 'Taux_Prot(%)']].head()


# #####   <font color='#21610B'> /// Contrôle résultat : Cas de l'avoine /// </font> La valeur Wikipedia etant : 10.7gr protéines / 100gr
# Ici je selectionne dans mon dataframe, les lignes dont le nom du produits est "Avoine" et je n'affiche que certaines colonnes avec ma selection q4sel

# In[27]:


q4t[q4t['PROD'] == "Avoine"][['CPAYS', 'PAYS'] + q4sel + ['QT_DISPROT', 'Taux_Prot(%)']].head()


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 5</u></font> : Aliments les plus caloriques :  Liste des 20 plus élevés
# 
# Comme précédemment on va calculer le ratio, mais cette fois par Produit/Pays.  
# Puis on fera une agregation et moyenne des ratios (Nrj/Poids) par pays en excluant les pays n'avant pas de data (pour la moyenne).  
# Dans un premier temps j'ai choisi de **rajouter** les colonnes **Ratio** et **Taux_Prot** au Dataframe principal **"gen"**.  
# Par la suite, je supprimerai du calcul les lignes Nan et inf.  
# Enfin, au lieu de faire une **somme** comme précédemment, je ferai une **moyenne** des ratio et taux par Produit/pays.

# #####   <font color='#61210B'>Recalcul Ratio et Taux par ligne et Ajout des Colonnes au Datafrane "gen"

# In[28]:


gen['RATIO(kcal/kg)']= gen['QT_DISPALI_KCAL']*365/gen['QT_DISPALI_KG']
gen['Taux_Prot(%)'] = (gen['QT_DISPROT']*365*100)/(gen['QT_DISPALI_KG']*1000)
gen.head()


# #####   <font color='#61210B'>Selection de Zones pour réaffichage

# In[29]:


q5sel = ['CPROD', 'PROD', 'CPAYS', 'PAYS', 'RATIO(kcal/kg)', 'Taux_Prot(%)']


# #####   <font color='#61210B'>MOYENNE des Ratio d'un produit tous pays confondus, Trié par Ratio décroissant
#     
# - Suppression des lignes dont le RATIO = 0
# - Suppression des lignes "NA"
# - Suppression des lignes "inf" (ici division par 0 donc test de la zone QT_DISPALI_KG)

# In[30]:


q5r = gen.copy()
q5r.drop(q5r[q5r['RATIO(kcal/kg)'] == 0].index, inplace=True)
q5r.replace(np.inf, np.nan)
# q5r.drop(q5r[q5r['QT_DISPALI_KG'] == 0].index, inplace=True)
q5r.dropna(subset=['RATIO(kcal/kg)'], inplace=True)


# In[31]:


q5r.groupby('PROD').mean().reset_index()
q5r.sort_values(['RATIO(kcal/kg)'], ascending=[False])[['CPROD', 'PROD', 
                                                        'RATIO(kcal/kg)', 'Taux_Prot(%)']].head(20)


# #####   <font color='#61210B'>MOYENNE des Taux de Protéines d'un produit tous pays confondus, Trié par Taux décroissant
#     
# - Suppression des lignes dont le Taux_Protéines = 0
# - Suppression des lignes "NA"
# - Suppression des lignes "inf" (ici division par 0 donc test de la zone QT_DISPALI_KG)

# In[32]:


q5t = gen.copy()
q5t.drop(q5t[q5t['Taux_Prot(%)'] == 0].index, inplace=True)
q5t.replace([np.inf, -np.inf], np.nan)
q5t.dropna(subset=['Taux_Prot(%)'], inplace=True)
q5t.sort_values(['Taux_Prot(%)'], ascending=[False])[['CPROD', 'PROD', 'RATIO(kcal/kg)', 'Taux_Prot(%)']].head(20)


# #####   <font color='#61210B'> /// Export des dataframes Calculés (q4r, q4t, q5) gen dans un fichier Excel pour contrôle futurs/// </font> Nom du fichier = PJ3_Ratios.xlsx

# In[33]:


writer = pd.ExcelWriter("OUTFILES/PJ3_Ratios.xlsx")
q4r.to_excel(writer,'Ratio')
q4t.to_excel(writer,'Taux_Prot')
q5r.to_excel(writer,'Max_Cal')
q5t.to_excel(writer,'Max_Prot')
writer.save()


# #####   <font color='#61210B'> /// Export du dataframe gen dans un fichier Excel pour contrôle futurs/// </font> Nom du fichier = PJ3_Bilan_Alim_gen_out.xlsx

# In[34]:


writer = pd.ExcelWriter("OUTFILES/PJ3_Bilan_Alim_gen_out.xlsx")
gen.to_excel(writer,'Sheet1')
writer.save()


# <p style="text-align:center";><font color='#38610B'><u>DataFrame "gen" - Détails des champs et définitions</u></p>
# 
# <img src="attachment:Dataframe-gen.png" width="500">

# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 6</u></font> : Calcul de la Disponibilité Intérieure mondiale pour les Végétaux
# 
# Exprimer le résultat en kcal

# On recupère le dataframe "gen" utilisé précédemment, on ne garde que les lignes "vegetaux" et on calcul le [QT_DISPINT]  
# Ici le Ratio est en ((kcal/kg/pers/an), la QT_DISPINT est en milliers_tonnes/pays/an.  
# 
# ATTENTION :   
# - Selectionner les lignes de type ['ORIG'] == 'vegetal'   (ou supprimer lignes "animal")
# - Supprimer les lignes RATIO=0  
# - Supprimer les lignes QT_DISPINT = 0
# - Supprimer lies lignes "inf"inite values
# 
# 
# - Calcul par pays/produit de QT_DI_VEG_KCAL1 (en Millions kcal/an ) avec
#       QT_DI_VEG_KCAL1 =  QT_DISPINT  *  RATIO(kcal/kg)
# 
# - Calcul par pays/produit de QT_DI_VEG_KCAL2 (en kcal/jour)
#       QT_DI_VEG_KCAL2 =  (QT_DISPINT  *  RATIO(kcal/kg) * 1'000'000  )  /   (VALP*365)

# In[35]:


q6 = gen[['PAYS', 'VALP', 'PROD', 'ORIG', 'QT_DISPINT', 'RATIO(kcal/kg)', 'Taux_Prot(%)']].copy()
q6.drop(q6[q6.ORIG == 'animal'].index, inplace=True)

q6['QT_DISPINT'] = q6['QT_DISPINT'].fillna(0)
q6['RATIO(kcal/kg)'] = q6['RATIO(kcal/kg)'].fillna(0)

q6['QT_DI_VEG_KCAL1'] = (q6['QT_DISPINT']*q6['RATIO(kcal/kg)'])
q6['QT_DI_VEG_KCAL2'] = (q6['QT_DI_VEG_KCAL1']*1000000)/(q6['VALP']*365)
q6.head()


# #####   <font color='#61210B'>Formule Dispo intérieure annuelle mondiale / personne (en kcal)
# 
# - DI_VEG(kcal/p/j) = Sum(QT_DI_VEG_KCAL1)* 1'000'000 /( 365 * pop_monde )  

# In[36]:


DI_VEG_kcal_p_j = q6['QT_DI_VEG_KCAL1'].sum()*1000000 / (365*pop_monde)
parm1 = "Disponibilité Intérieure Mondiale des 'végétaux' exprimée en Kcal: "
Markdown('<strong>{}</strong>{}{}'.format(parm1, round(DI_VEG_kcal_p_j, 3), " (Kcal/p/j)"))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 7</u></font> : Nb humains nourris en fonction de Disponibilité Intérieure mondiale des Végétaux
# 
# En calories, protéines, et pourcentage.  
#   
# <u>Estimation basée sur wiki et FAO </u>(source: https://fr.wikipedia.org/wiki/Prot%C3%A9ine#Quantit%C3%A9s_recommand%C3%A9es ) :  
# Les besoins moyens en protéines ont été définis par la FAO qui recommande 49 g de protéines pour les hommes adultes et 41 pour les femmes (47 si enceintes, 58,5 si allaitantes)  
# Il est extrémement difficile de trouver un chiffre "moyen" tant il y a de paramètres a prendre en compte.  
# Le sexe (homme/femme), le poids de la personne, le pays dans lequel elle vit, etc...   
# Pour l'exercice je vais prendre les données Wiki de cette source : https://fr.wikipedia.org/wiki/Apports_journaliers_recommand%C3%A9s  
# Énergie 	2 000 kcal  
# Protéines 	50 g
# 
# 

# On applique le même principe qu'à la question 6 pour les protéines  
# 
# - Calcul par pays/produit de QT_DI_VEG_PROT avec
#       QT_DI_VEG_PROT1 =  QT_DISPINT  *  Taux_Prot(%) * 1000 / 100
# 
# - Calcul en gr Protéines/jour
#       QT_DI_VEG_PROT2 =  (QT_DI_VEG_PROT1  * 1'000'000  )  /   (VALP*365)
# 
# 

# In[37]:


q7 = gen[['PAYS', 'VALP', 'PROD', 'ORIG', 'QT_DISPINT', 'RATIO(kcal/kg)', 'Taux_Prot(%)']].copy()
q7.drop(q7[q7.ORIG == 'animal'].index, inplace=True)

q7['QT_DISPINT'] = q7['QT_DISPINT'].fillna(0)
q7['Taux_Prot(%)'] = q7['Taux_Prot(%)'].fillna(0)

q7['QT_DI_VEG_PROT1'] = (q7['QT_DISPINT']*q7['Taux_Prot(%)']*1000) / 100 
q7['QT_DI_VEG_PROT2'] = (q7['QT_DI_VEG_PROT1']*1000000)/(q7['VALP']*365)
q7.head()


# #####   <font color='#61210B'>Formule Dispo intérieure annuelle mondiale / personne (en gr Protéines) :
# - DI_VEG(prot/p/j) = ∑(QT_DI_VEG_PROT1)* 1'000'000 /( 365 * pop_monde )

# In[38]:


DI_VEG_prot_p_j = q7['QT_DI_VEG_PROT1'].sum()*1000000 / (365*pop_monde)
parm1 = "Disponibilité Intérieure Mondiale des 'végétaux' exprimée en protéines: "
Markdown('<strong>{}</strong>{}{}'.format(parm1, round(DI_VEG_prot_p_j, 3), " (gr Protéines/p/j)"))


# #####   <font color='#61210B'>En exprimant ces resulats en (%) de la population mondiale :   
# Base de l'enoncé ci-dessus : 
# - Énergie 	2 000 kcal  
# - Protéines 	50 g

# In[39]:


var_wiki_nrj = 2000     # Variable - valeur wiki (en kcal) des besoins journalier d'un être humain
var_wiki_prot = 50      # Variable - valeur wiki (en gr protéines) des besoins journalier d'un être humain


# In[40]:


xcal = (DI_VEG_kcal_p_j*pop_monde)*100/(pop_monde*var_wiki_nrj)
xprot = (DI_VEG_prot_p_j*pop_monde)*100/(pop_monde*var_wiki_prot)
hcal = (xcal/100) * pop_monde
hprot = (xprot/100) * pop_monde


# In[41]:


display(HTML('<h3>Disponibilité Intérieure Mondiale de végétaux en Kcal</h3>'))
parm1 = str(round(xcal,2))
parm2 = "(%) des besoins mondiaux. Soit "
parm3 = str('{:15,.0f}'.format(hcal))
parm4 = " humains"
Markdown('<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4))


# In[42]:


display(HTML('<h3>Disponibilité Intérieure Mondiale de végétaux en Protéines</h3>'))
parm1 = str(round(xprot,2))
parm2 = "(%) des besoins mondiaux. Soit "
parm3 = str('{:15,.0f}'.format(hprot))
parm4 = " humains"
Markdown('<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 8</u></font> : Nb humains nourris en fonction de Disponibilité Alim. mondiale des Végétaux, nourriture végétale destinée aux animaux, et pertes de produits végétaux
# 
# En calories, protéines, et pourcentage.  
#   
# Comme pour les questions Q7/Q8, ici on va prendre la somme des 3 éléments ci-dessus en termes de quantité

# #####   <font color='#61210B'>Calculs en kcal

# In[43]:


q8 = gen[['PAYS', 'VALP', 'PROD', 'ORIG', 'QT_NOURRIT', 'QT_ALIMANI', 'QT_PERTES', 'RATIO(kcal/kg)', 
         'Taux_Prot(%)']].copy()
q8.drop(q8[q8.ORIG == 'animal'].index, inplace=True)
# Remplacer les valeurs NAN par 0 vant d'en faire la somme
q8.QT_NOURRIT = q8.QT_NOURRIT.fillna(0)
q8.QT_ALIMANI = q8.QT_ALIMANI.fillna(0)
q8.QT_PERTES = q8.QT_PERTES.fillna(0)
q8['RATIO(kcal/kg)'] = q8['RATIO(kcal/kg)'].fillna(0)

# Memorisation de la somme des Dispo Alim. nécessaires à la question
q8['QT_DA_CALC'] = q8['QT_NOURRIT'] + q8['QT_ALIMANI'] + q8['QT_PERTES']


q8['QT_DA_VEG_KCAL'] = (q8['QT_DA_CALC']*q8['RATIO(kcal/kg)'])
DA_VEG_kcal_p_j = q8['QT_DA_VEG_KCAL'].sum()*1000000 / (365*pop_monde)
q8.head()


# #####   <font color='#61210B'>Calculs en gr de Protéines

# In[44]:


q8 = gen[['PAYS', 'VALP', 'PROD', 'ORIG', 'QT_NOURRIT', 'QT_ALIMANI', 'QT_PERTES', 'RATIO(kcal/kg)', 
         'Taux_Prot(%)']].copy()
# Remplacer les valeurs NAN par 0 vant d'en faire la somme
q8.QT_NOURRIT = q8.QT_NOURRIT.fillna(0)
q8.QT_ALIMANI = q8.QT_ALIMANI.fillna(0)
q8.QT_PERTES = q8.QT_PERTES.fillna(0)

# Memorisation de la somme des Dispo Alim. nécessaires à la question
q8['QT_DA_CALC'] = q8['QT_NOURRIT'] + q8['QT_ALIMANI'] + q8['QT_PERTES']
q8.drop(q8[q8.ORIG == 'animal'].index, inplace=True)
q8.drop(q8[q8['QT_DA_CALC'] == 0].index, inplace=True)
q8.drop(q8[q8['Taux_Prot(%)'] == 0].index, inplace=True)
q8['QT_DA_VEG_PROT'] = (q8['QT_DA_CALC']*q8['Taux_Prot(%)']*1000) / 100 
DA_VEG_prot_p_j = q8['QT_DA_VEG_PROT'].sum()*1000000 / (365*pop_monde)
q8.head()


# In[45]:


display(HTML('<h4>Disponibilité Alimentaire Mondiale de végétaux + Nourriture Animaux + Pertes</h4>'))
parm1 = str(round(DA_VEG_kcal_p_j,3)) + " (kcal/pers/jour)"
parm2 = str(round(DA_VEG_prot_p_j,3)) + " (prot/pers/jour)"
Markdown('{}<br/>{}'.format(parm1, parm2))


# #####   <font color='#61210B'>Expression des resulats en (%) de la population mondiale. </font>  ---  Base utilisée : 
# - Énergie 	2 000 kcal  
# - Protéines 	50 g

# In[46]:


xcal = (DA_VEG_kcal_p_j*pop_monde)*100/(pop_monde*var_wiki_nrj)
xprot = (DA_VEG_prot_p_j*pop_monde)*100/(pop_monde*var_wiki_prot)
hcal = (xcal/100) * pop_monde
hprot = (xprot/100) * pop_monde


# In[47]:


display(HTML('<h3>Disponibilité Alimentaire Mondiale de végétaux + Nourriture Animaux + Pertes en Kcal</h3>'))
parm1 = "Elle représente "
parm2 = str(round(xcal,2))
parm3 = "(%) des besoins mondiaux. Soit "
parm4 = str('{:15,.0f}'.format(hcal))
parm5 = " humains"
Markdown('{}<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4,parm5))


# In[48]:


display(HTML('<h3>Disponibilité Alimentaire Mondiale de végétaux + Nourriture Animaux + Pertes en Protéines</h3>'))
parm1 = "Elle représente "
parm2 = str(round(xprot,2))
parm3 = "(%) des besoins mondiaux. Soit "
parm4 = str('{:15,.0f}'.format(hprot))
parm5 = " humains"
Markdown('{}<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4,parm5))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 9</u></font> : Nb humains nourris en fonction de Disponibilité Alimentaire Mondiale
# 
# En calories, protéines, et pourcentage.  
#   
# Ici, pas de calcul avec les ratio et taux(%)Prot comme pour les questions précédentes.
# On va prendre les données "standards" de la FAO, soient dans notre dataframe "gen", les colonnes :  
# - **QT_DISPALI_KCAL**  - Qté Disponibilité Alimentaire d'un produit/pays (en kcal/pers/jour)
# - **QT_DISPROT**  - Qté Disponibilité Protéines d'un produit/pays (en gr/pers/jour)
# 
# 

# In[49]:


q9 = gen[['CPAYS', 'PAYS', 'CPROD', 'PROD', 'ORIG', 'QT_DISPALI_KCAL', 'QT_DISPROT']].copy()
q9.head()


# #####   <font color='#61210B'>On regroupe par pays, et on fait la somme des kcal et protéines

# In[50]:


q9 = q9.groupby(['CPAYS', 'PAYS']).sum().reset_index()
q9.head()


# #####   <font color='#61210B'>On peut maintenant faire une moyenne mondiake des kcal et proteines et la comparer à notre base

# In[51]:


DA_KCAL_p_j = q9['QT_DISPALI_KCAL'].mean()
DA_PROT_p_j = q9['QT_DISPROT'].mean()
print("Dispo_Alimentaire_Mondiale(kcal/p/j) = ", round(DA_KCAL_p_j,3))
print("Dispo_Alimentaire_Mondiale(prot/p/j) = ", round(DA_PROT_p_j,3))


# In[52]:


parm1 = "Disponibilité Alimentaire Mondiale exprimée en Kcal: "
parm2 = "Disponibilité Alimentaire Mondiale exprimée en Protéines: "
Markdown('{}<strong>{}</strong>{}<br/>{}<strong>{}</strong>{}'.format
         (parm1, round(DA_KCAL_p_j, 3)," (Kcal/pers/jour)",
          parm2, round(DA_PROT_p_j, 3), " (gr Prot./pers/jour)"))


# #####   <font color='#61210B'>Expression des resulats en (%) de la population mondiale. </font>  ---  Base utilisée : 
# - Énergie 	2 000 kcal  
# - Protéines 	50 g

# In[53]:


xcal = (DA_KCAL_p_j*pop_monde)*100/(pop_monde*var_wiki_nrj)
xprot = (DA_PROT_p_j*pop_monde)*100/(pop_monde*var_wiki_prot)
hcal = (xcal/100) * pop_monde
hprot = (xprot/100) * pop_monde


# In[54]:


display(HTML('<h3>Disponibilité Alimentaire Mondiale en Kcal</h3>'))
parm1 = "Elle représente "
parm2 = str(round(xcal,2))
parm3 = "(%) des besoins mondiaux. Soit "
parm4 = str('{:15,.0f}'.format(hcal))
parm5 = " humains"
Markdown('{}<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4,parm5))


# In[55]:


display(HTML('<h3>Disponibilité Alimentaire Mondiale en Protéines</h3>'))
parm1 = "Elle représente "
parm2 = str(round(xprot,2))
parm3 = "(%) des besoins mondiaux. Soit "
parm4 = str('{:15,.0f}'.format(hprot))
parm5 = " humains"
Markdown('{}<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4,parm5))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 10</u></font> : Proportion de la population mondiale considérée en "sous-nutrition" - Année 2013
# 

# #####   <font color='#61210B'>Mise en forme du Dataframe ssn
# - Suppression de colonnes inutiles
# - Update de valeurs plus adequates (année, nb personnes)
# - Remplacer les NAN par '0' sur colonne numérique
# - Exclure la chine (code=351) car doublons avec autres lignes "chines" (voir question 1)

# In[56]:


q10 = ssn[['ANNEE', 'CZONE', 'ZONE', 'VAL', 'UNIT']].copy()
q10['NB_PERS_SSN'] = q10['VAL'] * 1000000
q10.drop(columns=['VAL', 'UNIT'], inplace=True)
q10.drop(q10[q10['ANNEE']=='2015-2017'].index, inplace=True)
q10.drop(q10[q10.CZONE == varcp_chine].index, inplace=True)
q10['ANNEE'] = np.where(q10['ANNEE']=='2012-2014', 2013, q10['ANNEE'])
q10.NB_PERS_SSN = q10.NB_PERS_SSN.fillna(0)
q10.head()


# #####   <font color='#61210B'>Resultat (%) population mondiale sous-alimentée

# In[57]:


TOT_POP_SSN = q10['NB_PERS_SSN'].sum()
prop = (TOT_POP_SSN*100/pop_monde)
print("Nb de personnes sous alimentée en 2013 : ", '{:10,.0f}'.format(TOT_POP_SSN), 
      "  - Cela représente ", round(prop,2), "(%) de la population mondiale")


# In[58]:


display(HTML('<h3>Nombre de Personnes sous-alimentées en 2013</h3>'))
parm1 = str('{:10,.0f}'.format(TOT_POP_SSN))
parm2 = " . Cela représente "
parm3 = str(round(prop,2))
parm4 = "(%) de la population mondiale"
Markdown('<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, parm3, parm4))


# #####   <font color='#61210B'> /// Export de la liste des pays en sous-nutrition dans un dataframe pour les questions Q12-13-14  /// </font> Nom du DF = ssn1

# In[59]:


ssn1 = q10[q10['NB_PERS_SSN']!=0].copy()


# #####   <font color='#61210B'> /// Export du dataframe q10 dans un fichier Excel pour contrôle futurs/// </font> Nom du fichier = PJ3_Q10-Sous_Nutrition_out.xlsx

# In[60]:


writer = pd.ExcelWriter("OUTFILES/PJ3_Q10-Sous_Nutrition_out.xlsx")
q10.to_excel(writer,'Sheet1')
writer.save()


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 11</u></font> : Proportion de céréales déstinées à l'alimentation animale - Année 2013
# 
# - Constitution de la liste de produits "type céréale" selon la FAO  
# - Calcul de la proportion sur ce périmètre

# In[61]:


cer.head()


# #####   <font color='#61210B'>Recherche sur sur dataframe "cer"
# - Liste des codes produits de type Céréales

# In[62]:


q11sel = cer['CPROD'].unique()
q11sel


# #####   <font color='#61210B'>Preparation des données à partir du dataframe principal "gen" 
#     
# - Selection des zones utiles : QT_NOURRIT (homme) & QT_ALIMANI (animal)
# - On remplace les valeurs NAN par 0 pour ne pas fausser les calculs  
# - On fait une somme Totale des céréales destinées à l'alimentation  (QT_CER_ALIM)

# In[63]:


tp11 = gen[['PAYS', 'VALP', 'CPROD', 'PROD', 'ORIG', 'QT_NOURRIT', 'QT_ALIMANI']].copy()
tp11.QT_NOURRIT = tp11.QT_NOURRIT.fillna(0)
tp11.QT_ALIMANI = tp11.QT_ALIMANI.fillna(0)
tp11['QT_CER_ALIM'] = tp11['QT_NOURRIT'] + tp11['QT_ALIMANI']
tp11.head()


# #####   <font color='#61210B'>Application du filtre des produits céréaliers sur ce dataframe temp</font>  --- Actions :
# 
# - 1°) Somme "mondiale" des colonnes numeriques : 
#     - TOT_NOURRIT = ∑ QT_NOURRIT
#     - TOT_ALIMANI = ∑ QT_ALIMANI
#     - TOT_CER_ALIM = ∑ QT_CER_ALIM
# - 2°) Calcul Proportion avec (TOT_ALIMANI) / (TOT_CER_ALIM)
# 

# In[64]:


q11 = tp11[tp11['CPROD'].isin(q11sel)]
q11.head()


# #####   <font color='#61210B'>Calcul de la proportion (%)

# In[65]:


TOT_NOURRIT = q11['QT_NOURRIT'].sum()
TOT_ALIMANI = q11['QT_ALIMANI'].sum()
TOT_CER_ALIM = q11['QT_CER_ALIM'].sum()
PROP = TOT_ALIMANI * 100 / TOT_CER_ALIM


# In[66]:


display(HTML("<h3>La proportion de céréales destinées à l'alimentation animale en 2013 est :</h3>"))
parm1 = str(round(PROP,2))
parm2 = "(%) de la production mondiale. Soit "
parm3 = " Millions de tonnes"
Markdown('<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1, parm2, round(TOT_ALIMANI/1000), parm3))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>Préparation des questions 12/13/14</u></font>
# 
# Sélection, parmi les données des bilans alimentaires, des informations relatives aux pays dans lesquels la FAO recense des personnes en sous-nutrition, pour une année choisie.
# 
# Repérage des 15 produits les plus exportés par ce groupe de pays sur l'année choisie.
# 
# Parmi les données des bilans alimentaires au niveau mondial, sélection des 200 plus grandes importations de ces produits (1 importation = une quantité d'un produit donné importée par un pays donné sur l'année choisie)
# 
# Regroupement des importations par produit, afin d'avoir une table contenant 1 ligne pour chacun des 15 produits.  
# Enfin, calcul pour chaque produit des 2 quantités suivantes :
# 
# - le ratio entre la quantité destinés aux "Autres utilisations" (Other uses) et la disponibilité intérieure.
# - le ratio entre la quantité destinée à la nourriture animale et la quantité destinée à la nourriture (animale + humaine)

# #####   <font color='#61210B'>Jointure Gauche entre :
# - Gauche >> Liste des pays en sous-nutrition - Dataframe **ssn1**
# - Droite >> Données Bilans Alimentaires      - Dataframe **gen**    
#     

# In[67]:


# Renommer les colonnes pour avoir les mêmes clefs avant jointure
ssn1.columns = ["ANNEE", "CPAYS", "PAYS", "NBPERS"]
# Changer le type de la colonne en float64 avant merge
ssn1[['ANNEE']] = ssn1[['ANNEE']].astype(int)


# In[68]:


tp12 = gen[['CPAYS', 'PAYS', 'CPROD', 'PROD', 'QT_IMPORT', 'QT_EXPORT', 
            'QT_DISPINT', 'QT_AUTRES', 'QT_ALIMANI', 'QT_NOURRIT']].copy()
tp = pd.merge(ssn1, tp12, how="left")
tp['QT_IMPORT'] = tp['QT_IMPORT'].fillna(0)
tp['QT_EXPORT'] = tp['QT_EXPORT'].fillna(0)
tp['QT_DISPINT'] = tp['QT_DISPINT'].fillna(0)
tp['QT_ALIMANI'] = tp['QT_ALIMANI'].fillna(0)
tp['QT_AUTRES'] = tp['QT_AUTRES'].fillna(0)
tp['QT_NOURRIT'] = tp['QT_NOURRIT'].fillna(0)
tp.head()


# #####   <font color='#61210B'>Détermination des 15 produits les plus exportés sur cette selection de pays
# - Regroupement par Produit des QT exportées
# - Tri décroissant des 15 premières lignes
#     

# In[69]:


s15 = tp.groupby(['CPROD', 'PROD'])['QT_EXPORT'].sum().reset_index()
s15 = s15.sort_values(['QT_EXPORT'], ascending=[False]).head(15)
s15.columns = ["CPROD", "PROD", "TOT_EXPORT"]
s15


# #####   <font color='#61210B'>Pour ces 15 produits sélectionnés, choisir les 200 plus grandes importations
# - 1 importation = une quantité d'un produit donné importée par un pays donné

# In[70]:


s200 = pd.merge(s15, tp, how="left")
s200 = s200.sort_values(['QT_IMPORT'], ascending=[False]).head(200)
s200.tail()


# #####   <font color='#61210B'>On regroupe ces 200 lignes à nouveau par produit pour faire des calculs de ratio suivants :
# 
# -   le ratio entre la quantité destinés aux "Autres utilisations" (Other uses) et la disponibilité intérieure.
# -   le ratio entre la quantité destinée à la nourriture animale et la quantité destinée à la nourriture (animale + humaine)
# 

# In[71]:


q12 = s200.groupby(['CPROD', 'PROD'])['QT_IMPORT', 'QT_EXPORT', 'QT_DISPINT', 'QT_AUTRES', 
                                      'QT_ALIMANI', 'QT_NOURRIT'].sum().reset_index()
q12.columns = ['CPROD', 'PROD', 'TOT_IMPORT', 'TOT_EXPORT', 'TOT_DISPINT', 'TOT_AUTRES', 
                                      'TOT_ALIMANI', 'TOT_NOURRIT']
q12.head()


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 12</u></font> : 3 Produits ayant les plus forts ratios 
# - #### Ratio 1 = entre la quantité destinés aux "Autres utilisations" (Other uses) et la disponibilité intérieure.   
# - #### Ratio 2 = entre la quantité destinée à la nourriture animale et la quantité destinée à la nourriture (animale + humaine).

# In[72]:


q12['Ratio1(%)'] = q12['TOT_AUTRES'] *100 / q12['TOT_DISPINT']
q12['Ratio2(%)'] = q12['TOT_ALIMANI'] *100 / (q12['TOT_ALIMANI']+q12['TOT_NOURRIT'])
q12
#q12[(q12['CPROD'] == 2577)].head()


# In[73]:


display(HTML("<h3>Les 3 Produits ayant le Ratio1(%) le plus élevé sont :</h3>"))
display(HTML("Ratio 1 = QT 'Autres utilisations'(Other uses) / QT Disponibilité Intérieure"))
q12.sort_values(['Ratio1(%)'], ascending=[False])[['PROD', 'Ratio1(%)']].head(3)


# #####   <font color='#61210B'>Les 3 Produits ayant le Ratio2(%) le plus élevé sont :

# In[74]:


display(HTML("<h3>Les 3 Produits ayant le Ratio2(%) le plus élevé sont :</h3>"))
display(HTML("Ratio 1 = QT Nourriture animale / (QT Nourriture animale + QT Nourriture humaine)"))
q12.sort_values(['Ratio2(%)'], ascending=[False])[['PROD', 'Ratio2(%)']].head(3)


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 13</u></font> : Tonnes de Céréales libérées, si les USA baissent de 10% la production de produits animaliers

# - Selection à partir du DataFrame général des lignes pour le Code Pays "Etats-Unis" (231)  

# In[75]:


tp13 = gen[(gen['CPAYS'] == 231)][['CPAYS', 'PAYS', 'CPROD', 'PROD', 'QT_ALIMANI']].copy()
tp13.head()


# - Jointure ou  Filtre sur la liste de produits de type "céréales" q11sel  (voir Question 11)

# In[76]:


tp13['QT_ALIMANI'] = tp13['QT_ALIMANI'].fillna(0)
q13 = tp13[tp13['CPROD'].isin(q11sel)]
tot_prod_animali_usa = q13['QT_ALIMANI'].sum()
eco = 0.1 * (tot_prod_animali_usa * 1000)


# In[77]:


display(HTML("<h3>En 2013, si les Etats-Unis avaient baissé leur production de produits animaliers de 10%,</h3>"))
parm1 = str('{:15,.0f}'.format(eco))
parm2 = " tonnes de céréales auraient été libérées"
Markdown('<strong>{}</strong>{}'.format(parm1,parm2))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 14</u></font> : Thaïlande  -  Calculs de proportions  :
# 
# - Proportion de manioc exportée
# - Proportion de personnes en sous-nutrition

# - Selection à partir du DataFrame général des lignes pour le Code Pays "Thailande" (216)  

# In[78]:


q14 = gen[(gen['CPAYS'] == 216)][['CPAYS', 'PAYS', 'VALP', 'CPROD', 'PROD', 'QT_EXPORT', 'QT_PRODUCT']].copy()
q14['QT_EXPORT'] = q14['QT_EXPORT'].fillna(0)
q14.head()


# - Calcul du Total des quantités exportées par la Thailande en tonnes (2013)

# In[79]:


QT_TOT_EXP_THAI = q14['QT_EXPORT'].sum()
parm1 = "Total des Exportations de la Thailande en 2013 : "
parm2 = str('{:15,.2f}'.format(QT_TOT_EXP_THAI/1000))
parm3 = " (Millions de Tonnes)"
Markdown('<strong><u>{}</u><br/>{}</strong>{}'.format(parm1,parm2,parm3))


# - Recherche de la quantité de manioc exportée par la Thailande en tonnes (2013)  ---  Code Produit [2532]

# In[80]:


QT_MANIOC_EXP_THAI = q14[(q14['CPROD'] == 2532)]['QT_EXPORT'].mean()
TX_MANIOC_EXP = QT_MANIOC_EXP_THAI *100 / QT_TOT_EXP_THAI


# In[81]:


TX_MANIOC_PRD = q14[(q14['CPROD'] == 2532)]['QT_EXPORT'].max() / q14[(q14['CPROD'] == 2532)]['QT_PRODUCT'].max()


# In[82]:


display(HTML("<h3><u>En 2013, la Thaïlande a exporté</u></h3>"))
parm1 = str('{:15,.1f}'.format(round(QT_MANIOC_EXP_THAI/1000,1)))
parm2 = " Millions de tonnes de manioc."
parm3 = " Cela représente "
parm4 = str('{:15,.1f}'.format(round(TX_MANIOC_EXP,3)))
parm5 = " (%) des Exports du pays."
parm6 = " Cela représente aussi "
parm7 = str('{:15,.2f}'.format(TX_MANIOC_PRD * 100))
parm8 = " (%) de la production annuelle de manioc"
Markdown('<strong>{}</strong>{}{}<strong>{}</strong>{}<br/>{}<strong>{}</strong>{}'.
         format(parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8))


# - Recherche de la population de la Thailande dans le dataframe pop (2013)  ---  Code Pays [216]

# In[83]:


POP_THAI = pop[(pop['CPAYS'] == 216)]['VALP'].max()


# - Recherche du nombre de personne sous-alimentée en Thailande dans le dataframe des pays en sous-nutrition "ssn1" (exporté à la question 10)

# In[84]:


NBP_SSN_THAI = ssn1[(ssn1['CPAYS'] == 216)]['NBPERS'].max()
TXP_SSN_THAI = NBP_SSN_THAI * 100 / POP_THAI


# #####   <font color='#61210B'>Calcul de la proportion de personnes en sous-nutrition en thailande représente 9.1(%) de la population du pays (2013)

# In[85]:


print(round(TXP_SSN_THAI,3), "(%), soit environ ", '{:8,.0f}'.format(NBP_SSN_THAI), " thaïlandais")

display(HTML("<h3><u>En 2013, la proportion de personnes en sous-nutrition en thailande représente</u></h3>"))
parm1 = str('{:15,.1f}'.format(TXP_SSN_THAI)) + "(%)"
parm2 = " de la population du pays. Soit "
parm3 = str('{:8,.0f}'.format(NBP_SSN_THAI))
Markdown('<strong>{}</strong>{}<strong>{}</strong>{}'.format(parm1,parm2,parm3," thaïlandais"))


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>QUESTION 15 - 20</u></font> : EXPORT DES DATAFRAMES en CSV
# 
# - Pour utilisation avec SGBD SQL  :   MySQL ou SQLite3  
# Ici nous rechargeons des données de la FAOSTAT pour prendre en compte plusieurs années (2012 et la dernière disponible)

# In[86]:


get_ipython().run_line_magic('cd', 'SQL')


# #####   <font color='#61210B'>Table "population"
# - Clé primaire proposée :  ANNEE / CPAYS

# In[87]:


popsql = pd.read_csv("FAOSTAT_pop_2012-2017.csv")
popsql.columns = ["xx", "xx", "CPAYS", "PAYS", "xx", "xx", "xx", "xx", "xx", 
               "ANNEE", "UNIT", "VALP", "xx", "xx", "xx"]
popsql.drop(columns=['xx'], inplace=True)
popsql.drop(columns=['UNIT'], inplace=True)
popsql.drop(popsql[popsql.CPAYS == varcp_chine].index, inplace=True)
popsql['VALP'] = round(popsql['VALP'] * 1000)
cols =  ['ANNEE', 'CPAYS', 'PAYS', 'VALP']
popsql = popsql[cols]
popsql.to_csv('sql_population.csv', sep=',', encoding='utf-8', index=False)
popsql.head()


# #####   <font color='#61210B'>Table "dispo_alim"
# Selection avant export des colonnes requises :  
# (pays, code_pays, année, produit, code_produit, origin, dispo_alim_tonnes, dispo_alim_kcal_p_j, dispo_prot, dispo_mat_gr)
# - Clé Primaire proposée : ANNEE / CPAYS / CPROD

# In[88]:


anisql = pd.read_csv("FAOSTAT_ani_2012-2013.csv")
anisql.columns = ["xx", "xx", "CPAYS", "PAYS", "CELEM", "ELEMENT", "CPROD", "PROD", "xx", 
               "ANNEE", "UNIT", "VAL", "xx", "xx"]
anisql.drop(columns=['xx'], inplace=True)
anisql["ORIG"] = "animal"


# In[89]:


vegsql = pd.read_csv("FAOSTAT_veg_2012-2013.csv")
vegsql.columns = ["xx", "xx", "CPAYS", "PAYS", "CELEM", "ELEMENT", "CPROD", "PROD", "xx", 
               "ANNEE", "UNIT", "VAL", "xx", "xx"]
vegsql.drop(columns=['xx'], inplace=True)
vegsql["ORIG"] = "vegetal"


# In[90]:


tempsql = anisql.append(vegsql)


# In[91]:


gensql = tempsql.pivot_table(
    index=["CPAYS","PAYS","ANNEE", "CPROD","PROD","ORIG"],
    columns = ["CELEM", "ELEMENT", "UNIT"], values=["VAL"], aggfunc=sum)
gensql.columns = ['QT_DISPALI_KG', 'QT_DISPALI_KCAL', 'QT_DISPROT', 'QT_DISPMG', 'QT_VARSTOCK', 'QT_PERTES',
                'QT_TRANSF', 'QT_NOURRIT', 'QT_AUTRES', 'QT_DISPINT', 'QT_PRODUCT', 'QT_ALIMANI', 
                'QT_SEMENCES', 'QT_IMPORT', 'QT_EXPORT']
gensql = gensql.reset_index()
gensql.drop(gensql[gensql.CPAYS == varcp_chine].index, inplace=True)


# In[92]:


cols =  ['ANNEE', 'CPAYS', 'PAYS', 'CPROD', 'PROD', 'ORIG',
            'QT_DISPALI_KG', 'QT_DISPALI_KCAL', 'QT_DISPROT', 'QT_DISPMG']
q16 = gensql.copy()
q16 = q16[cols]
q16['QT_DISPALI_KG'] = q16['QT_DISPALI_KG'] * 1000
q16.rename(columns={'QT_DISPALI_KG': 'QT_DISPALI_T'}, inplace=True)

q16.QT_DISPALI_T    = q16.QT_DISPALI_T.fillna(0)
q16.QT_DISPALI_KCAL = q16.QT_DISPALI_KCAL.fillna(0)
q16.QT_DISPROT      = q16.QT_DISPROT.fillna(0)
q16.QT_DISPMG       = q16.QT_DISPMG.fillna(0)

q16.to_csv('sql_dispo_alim.csv', sep=',', encoding='utf-8', index=False)
q16.head()


# #####   <font color='#61210B'>Table "equilibre_prod"
# Selection avant export des colonnes requises :  
# (pays, code_pays, année, produit, code_produit, dispo_int, alim_ani, semences, pertes, transfo, nourriture, autres_utilisations)
# - Clé Primaire proposée : ANNEE / CPAYS / CPROD

# In[93]:


q17 = gensql[['ANNEE', 'CPAYS', 'PAYS', 'CPROD', 'PROD', 'ORIG', 'QT_DISPINT', 'QT_ALIMANI',
           'QT_SEMENCES', 'QT_PERTES', 'QT_TRANSF', 'QT_NOURRIT', 'QT_AUTRES']].copy()

q17.QT_DISPINT  = q17.QT_DISPINT.fillna(0)
q17.QT_ALIMANI  = q17.QT_ALIMANI.fillna(0)
q17.QT_SEMENCES = q17.QT_SEMENCES.fillna(0)
q17.QT_PERTES   = q17.QT_PERTES.fillna(0)
q17.QT_TRANSF   = q17.QT_TRANSF.fillna(0)
q17.QT_NOURRIT  = q17.QT_NOURRIT.fillna(0)
q17.QT_AUTRES   = q17.QT_AUTRES.fillna(0)

q17.to_csv('sql_equilibre_prod.csv', sep=',', encoding='utf-8', index=False)
q17.head()


# #####   <font color='#61210B'>Table "sous-nutrition"
# Le même principe de la question Q10 peut être utilisé ici.
# 
# - Clé Primaire proposée : ANNEE / CPAYS

# In[94]:


q18 = ssn[['ANNEE', 'CZONE', 'ZONE', 'VAL', 'UNIT']].copy()
q18['NB_PERS_SSN'] = q18['VAL'] * 1000000
q18.drop(columns=['VAL', 'UNIT'], inplace=True)
q18.drop(q18[q18.CZONE == varcp_chine].index, inplace=True)
q18['ANNEE'] = np.where(q18['ANNEE']=='2012-2014', 2013, q18['ANNEE'])
q18['ANNEE'] = np.where(q18['ANNEE']=='2015-2017', 2016, q18['ANNEE'])
q18.NB_PERS_SSN = q18.NB_PERS_SSN.fillna(0)
q18.rename(columns={'CZONE': 'CPAYS'}, inplace=True)
q18.rename(columns={'ZONE': 'PAYS'}, inplace=True)
q18.to_csv('sql_sous-nutrition.csv', sep=',', encoding='utf-8', index=False)
q18.head()


# In[95]:


dureetotale = round(time.time() - trt_start_time, 5)
print("--- Durée TOTALE du Notebook PJ3 --- ", "%s seconds" % dureetotale)

