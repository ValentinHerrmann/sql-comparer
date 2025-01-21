SELECT regierungsbezirk, SUM(einwohner_m), SUM(einwohner_w)
FROM gemeinde
GROUP BY regierungsbezirk