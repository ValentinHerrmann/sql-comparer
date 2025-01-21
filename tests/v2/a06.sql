SELECT name, kreis, flaeche, einwohner_m, einwohner_w
FROM Gemeinde 
WHERE (einwohner_m > 50000 AND einwohner_w > 50000) OR flaeche > 100