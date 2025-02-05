SELECT betreiber, ort
FROM Ladestation
WHERE bundesland="Bayern"
  AND ort != "München"