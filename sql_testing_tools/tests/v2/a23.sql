SELECT name, einwohner_m, einwohner_w 
FROM Gemeinde 
WHERE NOT name LIKE 'München' and einwohner_m > 1000
