With T1 as (
Select 	CPAYS, PAYS, ANNEE,
 		round(sum(d.QT_DISPALI_KCAL),2) DA_KCAL_P_J1
From 	dispo_alim d 
Where   QT_DISPALI_KCAL is not NULL
Group by CPAYS, PAYS, ANNEE
Order by CPAYS, ANNEE)
Select CPAYS, PAYS, round(avg(DA_KCAL_P_J1),2)  as DA_KCAL_P_J
From   T1
Group by CPAYS
Order by DA_KCAL_P_J desc
Limit 10
;

With T2 as (
Select 	CPAYS, PAYS, ANNEE,
 		round(sum(d.QT_DISPROT),2) DA_PROT_GR_P_J1
From 	dispo_alim d 
Where   QT_DISPROT is not NULL
Group by CPAYS, PAYS, ANNEE
Order by CPAYS, ANNEE)
Select CPAYS, PAYS, round(avg(DA_PROT_GR_P_J1),2)  as DA_PROT_GR_P_J
From   T2
Group by CPAYS
Order by DA_PROT_GR_P_J desc
Limit 10
;

