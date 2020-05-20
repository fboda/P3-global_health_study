With Result As (
Select 	ANNEE, CPAYS, PAYS, sum(QT_DISPROT) DA_CALC, 
		row_number() over(partition by ANNEE Order by sum(QT_DISPROT)) as Rn
From 	dispo_alim
Where   QT_DISPROT is not NULL 
Group by ANNEE, CPAYS, PAYS)
Select ANNEE, CPAYS, PAYS, round(DA_CALC/1000, 3) DA_PROT_KG_HAB
From Result Where  Rn <= 10 ;

