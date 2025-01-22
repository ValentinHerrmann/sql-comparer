SELECT name, einwohner_m, einwohner_w 
FROM Gemeinde 
WHERE flaeche > 150 OR einwohner_m > 75000 OR einwohner_w > 75000