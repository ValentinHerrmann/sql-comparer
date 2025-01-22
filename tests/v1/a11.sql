SELECT COUNT(*)
FROM Schwimmbad, Gemeinde
WHERE Gemeinde.schluessel = Schwimmbad.gemeindeschluessel
AND Gemeinde.einwohner_w > 1000