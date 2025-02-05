SELECT betreiber, ort
FROM Ladestation
WHERE not bundesland="Bayern"
  AND ort != "München"