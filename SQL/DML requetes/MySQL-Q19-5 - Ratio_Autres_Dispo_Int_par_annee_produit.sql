With Result As (
Select 	ANNEE, CPROD, PROD,
		sum(QT_AUTRES)/sum(QT_DISPINT) RATIO,
        row_number() over(partition by ANNEE Order by sum(QT_AUTRES)/sum(QT_DISPINT) desc) as Rn
From  	equilibre_prod
Where   QT_DISPINT <> 0 and QT_AUTRES <> 0
Group By ANNEE, CPROD, PROD)
Select ANNEE, CPROD, PROD, round(RATIO, 5) RATIO_AUTRES_DISPINT
From Result Where  Rn <= 10 ;


