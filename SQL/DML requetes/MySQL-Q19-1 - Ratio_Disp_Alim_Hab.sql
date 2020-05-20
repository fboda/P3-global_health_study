Select 	CPAYS, PAYS, round(sum(QT_DISPALI_KCAL),2) DA_KCAL_P_J_2013
From 	dispo_alim  
Where   ANNEE = 2013 and QT_DISPALI_KCAL is not NULL
Group by CPAYS, PAYS
Order by DA_KCAL_P_J_2013 desc
Limit 10;



Select 	CPAYS, PAYS, round(sum(QT_DISPROT),2)/1000 DA_PROT_KG_P_J_2013
From 	dispo_alim 
Where   ANNEE = 2013 and QT_DISPROT is not NULL
Group by CPAYS, PAYS
Order by DA_PROT_KG_P_J_2013 desc
Limit 10;

