SELECT name, einwohner_m, einwohner_w 
FROM Gemeinde 
WHERE NOT name LIKE 'München'
