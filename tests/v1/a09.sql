SELECT COUNT(*), SUM(einwohner_w), regierungsbezirk, AVG(einwohner_m)
FROM gemeinde
GROUP BY regierungsbezirk