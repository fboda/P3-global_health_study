SELECT code_pays, pays, round(sum(dispo_alim_kcal_p_j),2) DA_KCAL_P_J_2013
FROM   dispo_alim 
WHERE  annee = 2013 and dispo_alim_kcal_p_j is not null     
GROUP BY code_pays, pays
ORDER BY DA_KCAL_P_J_2013 DESC
LIMIT 10;



SELECT code_pays, pays, round(sum(dispo_prot),2) DA_PROT_GR_P_J_2013
FROM   dispo_alim
WHERE  annee = 2013 and dispo_prot is not null     
GROUP BY code_pays, pays
ORDER BY DA_PROT_GR_P_J_2013 DESC
LIMIT 10;
