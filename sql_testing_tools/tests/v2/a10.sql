SELECT regierungsbezirk, avg(flaeche), kreis
FROM Gemeinde
GROUP BY kreis,regierungsbezirk
