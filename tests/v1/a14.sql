SELECT Gemeinde.name
FROM Gemeinde,Wanderweg_zu_Gemeinde
WHERE Gemeinde.schluessel = Wanderweg_zu_Gemeinde.gemeindeschluessel
AND (Gemeinde.regierungsbezirk='Oberbayern' OR Gemeinde.regierungsbezirk='Niederbayern')