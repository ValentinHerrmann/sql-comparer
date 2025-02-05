SELECT name, einwohner_m, einwohner_w 
FROM Gemeinde 
WHERE einwohner_m > 1000 AND name != 'München'
