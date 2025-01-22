SELECT Zoo.name
FROM Zoo,Gemeinde
WHERE Gemeinde.name='Erlangen' AND Zoo.gemeindeschluessel = Gemeinde.schluessel