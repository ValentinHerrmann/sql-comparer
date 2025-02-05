Select AVG(leistung), id
From Ladesteckdose
Group by typ
Order by typ ASC
Where typ LIKE "DC %"