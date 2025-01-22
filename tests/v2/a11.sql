SELECT COUNT(*)
FROM Schwimmbad, Gemeinde
WHERE Gemeinde.einwohner_w > 1000 AND Gemeinde.schluessel = Schwimmbad.gemeindeschluessel