With T1 as (
Select 	code_pays, pays, annee,
 		round(sum(d.dispo_alim_kcal_p_j),2) DA_KCAL_P_J1
From 	dispo_alim d 
Where   dispo_alim_kcal_p_j is not NULL
Group by code_pays, pays, annee
Order by code_pays, annee)

    Select   code_pays, pays, round(avg(DA_KCAL_P_J1),2)  as DA_KCAL_P_J
    From     T1
    Group by code_pays
    Order by DA_KCAL_P_J desc
    Limit 10
;




With T2 as (
Select 	code_pays, pays, annee,
 		round(sum(d.dispo_prot),2) DA_PROT_GR_P_J1
From 	dispo_alim d 
Where   dispo_prot is not NULL
Group by code_pays, pays, annee
Order by code_pays, annee)

    Select   code_pays, pays, round(avg(DA_PROT_GR_P_J1),2)  as DA_PROT_GR_P_J
    From     T2
    Group by code_pays
    Order by DA_PROT_GR_P_J desc
    Limit 10
;

