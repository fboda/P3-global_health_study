Select 	annee, pays, sum(pertes*1000000) as Pertes_Kg
From  	equilibre_prod
Group By annee, pays
