SELECT regierungsbezirk, SUM(einwohner_w), AVG(einwohner_m), COUNT(*)
FROM gemeinde
GROUP BY regierungsbezirk