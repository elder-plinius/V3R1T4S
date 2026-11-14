# success_criterion (verbatim from bank/targets.json)

Target id: `catagolue-glider-synthesis-cost-records`

Success means an RLE pattern in rule B3/S23 that (1) at generation 0 consists ONLY of gliders, each a separate connected component, (2) is a valid synthesis: rewinding every glider backwards by at least 4*(bounding box diameter) generations along its own trajectory produces a pattern with no glider-glider interaction during the rewound interval (so the gliders genuinely come in from infinity), (3) after running forward until the population is periodic, contains exactly the target object (apgcode match, via lifelib or an independent simulator) with NO other live cells and no escaping gliders or spaceships (unless the page's own synthesis convention for that object explicitly allows outgoing gliders, in which case follow it literally), and (4) uses STRICTLY fewer gliders than the cost shown for that apgcode on its Catagolue object page and tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/<class>), re-fetched live immediately before claiming. For objects listed with a '(pseudo)' cost, compare against that listed number but report the result as a true synthesis improvement only if the new synthesis is all-glider. A first synthesis of a strict still life or oscillator absent from the tables also counts if its apgcode does not appear on the tabulation page for its class.

## partial_wins p1 (relevant)

A strictly cheaper true glider synthesis for any object whose current listed cost is at least 60 gliders, verified as above.

## status_source

https://catagolue.hatsya.com/syntheses
