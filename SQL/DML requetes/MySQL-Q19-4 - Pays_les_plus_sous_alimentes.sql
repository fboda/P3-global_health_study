Select 	ssn.ANNEE, ssn.CPAYS, ssn.PAYS, 
		round((ssn.nb_pers_ssn / pop.valp)*100, 2) Taux_p_ssn
From 	sous_nutrition ssn Inner Join population pop
On 		ssn.annee = pop.annee and ssn.cpays = pop.cpays
Order by Taux_p_ssn desc
Limit 10
;




