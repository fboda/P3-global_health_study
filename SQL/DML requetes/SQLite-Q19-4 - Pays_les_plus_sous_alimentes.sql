Select 	ssn.annee, ssn.code_pays, ssn.pays, 
		round((ssn.nb_personnes / pop.population)*100, 2) Taux_p_ssn
From 	sous_nutrition ssn Inner Join population pop
On 	ssn.annee = pop.annee and ssn.code_pays = pop.code_pays
Order by Taux_p_ssn desc
Limit 10
;
