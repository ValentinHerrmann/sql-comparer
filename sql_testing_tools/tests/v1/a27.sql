SELECT typ, avg(leistung)
FROM Ladesteckdose
WHERE typ LIKE "DC %"
GROUP BY typ
ORDER BY typ