SELECT name, einwohner_m, einwohner_w 
FROM Gemeinde 
WHERE (einwohner_m > 75000 OR flaeche > 150 OR 75000 < einwohner_w)