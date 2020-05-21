<hr style="height: 4px; color: #839D2D; width: 100%; ">

# Etude de santé publique mondiale

<hr style="height: 2px; color: #839D2D; width: 100%; ">

Formation ENSAE / OpenClassRooms   -   Parcours DATA ANALYST
### Réaliser une étude de grande ampleur sur le thème de la sous-nutrition dans le monde.
Les données sont issues du site de la FAO (<http://www.fao.org/faostat/fr/#data>).  
Voici les critères de téléchargement ainsi que les DataFrames pandas contenant ces tables/fichiers :  
* DataFrame <strong>ani</strong> : Bilan Alimentaire Produits Animaliers <br>
  Filtre > (**Pays** = tous, **Eléments** = tous, **Année** = 2013, **Groupe Produits** = Produits Animaux(liste) )
* DataFrame <strong>veg</strong> : Bilan Alimentaire Produits Vegetaux <br>
  Filtre > (**Pays** = tous, **Eléments** = tous, **Année** = 2013, **Groupe Produits** = Produits Végétaux(liste) )
* DataFrame <strong>pop</strong> : Bilan Alimentaire Produits Vegetaux <br>
  Filtre > (**Pays** = tous, **Eléments** = population totale, **Année** = 2013, **Produits** = Population )
* DataFrame <strong>ssn</strong> : Sous-Nutrition en Nb.personnes/Pays <br>
  Filtre > (**Pays** = tous, **Eléments** = population totale, **Année** = 2013-2016, **Produits** = Population )
* DataFrame <strong>cer</strong> : Bilan Produits Type "cérèales" <br>
  Filtre > (**Pays** = Monde, **Eléments** = tous, **Année** = 2013, **Groupe Produits** = Cérèales-Excl bière>(liste) )
<br />&nbsp;<br />
**<font color='#38610B'>- Date : 18 Dec 2018</font>**  
Auteur : Frédéric Boissy
<hr style="height: 4px; color: #839D2D; width: 100%; ">
