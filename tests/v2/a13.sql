SELECT COUNT(*)
FROM Gemeinde, Radweg_zu_Gemeinde
WHERE Gemeinde.plz > 96400 AND Gemeinde.schluessel=Radweg_zu_Gemeinde.gemeindeschluessel