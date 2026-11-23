fetching https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL244_Ki.csv
PASS  csv sha256 b296c5956c9b3659
PASS  cliff test molecules >= 40 296
PASS  test/train sizes 621/2476 
PASS    object\M1_predictions.json indices exact 
PASS    object\M1_predictions.json sha recorded 
PASS    object\M1_predictions.json one y per test molecule 
PASS    object\B_predictions.json indices exact 
PASS    object\B_predictions.json sha recorded 
PASS    object\B_predictions.json one y per test molecule 
M1  cliff 0.550194338 noncliff 0.333430391
B   cliff 0.634573831 noncliff 0.399310626
PASS  cliff MSE strictly lower delta 0.084379
PASS  noncliff not worse delta -0.065880
PASS  B == repo-config SVR recomputed max diff 0.00e+00
PASS  no InChIKey train/test overlap 
VERIFY_P2: PASS
