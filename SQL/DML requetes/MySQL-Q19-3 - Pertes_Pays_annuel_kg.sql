Select 	ANNEE, PAYS, sum(QT_PERTES*1000000) as PERTES_KG
From  	equilibre_prod
Group By ANNEE, PAYS
