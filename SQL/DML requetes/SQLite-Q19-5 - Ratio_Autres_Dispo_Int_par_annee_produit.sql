With 
T1 As (
Select Distinct Annee from equilibre_prod a
Order by Annee)
,
T2 As (
Select 	annee, code_produit, produit, round(sum(autres_utilisations)/sum(dispo_int),5) RATIO
From 	equilibre_prod
Where   autres_utilisations <> 0 and dispo_int <> 0
Group by annee, code_produit, produit
Order by RATIO desc
Limit 20)

Select T1.annee, T2.code_produit, T2.produit, T2.RATIO
From   T1 Join T2 On T1.annee = T2.annee
Order by T1.annee 