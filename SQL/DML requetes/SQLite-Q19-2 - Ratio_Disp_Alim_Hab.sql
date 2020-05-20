With 
T1 As (
Select Distinct Annee from dispo_alim a
Order by Annee)
,
T2 As (
Select 	annee, code_pays, pays, round(sum(dispo_prot)/1000,3) DA_CALC
From 	dispo_alim
Where   dispo_prot is not NULL 
Group by annee, code_pays, pays
Order by DA_CALC
Limit 20)

Select T1.annee, T2.code_pays, T2.pays, T2.DA_CALC
From   T1 Join T2 On T1.annee = T2.annee
Order by T1.annee 