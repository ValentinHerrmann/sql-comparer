SELECT name, kreis, flaeche, einwohner_m, einwohner_w
FROM Gemeinde 
WHERE (einwohner_w > 50000 OR einwohner_m > 50000) AND flaeche > 100 