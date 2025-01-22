SELECT name, kreis, flaeche, einwohner_m, einwohner_w
FROM Gemeinde 
WHERE flaeche > 100 OR (einwohner_w > 50000 AND einwohner_m > 50000)