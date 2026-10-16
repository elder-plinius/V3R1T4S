# Run it yourself (from this folder, fresh shell)
sh verify-it-yourself/run_checks.sh
# expected: E=-4581.205775329242058388545669185821859506, grad_norm=7.173e-27, margin=0.000880329..., last line PASS
# Hessian and distinct basin (needs numpy, scipy, mpmath):
python3 how-we-built-it/check.py object/LJ662.xyz.txt -4581.204895 --hess   # expect n_neg=0 n_zero=6, BEATS_RECORD_BY_1e-5=True
# Table basin: download https://doye.chem.ox.ac.uk/jon/structures/LJ/LJ562-1000.tar.gz, extract 662.TXT, then
python3 how-we-built-it/check.py 662.TXT -4581.204895 --hess                # expect E_polished -4581.204913258
# Rebuild the object: remove the least-bound atom from table 663.TXT and relax (how-we-built-it/sweep.py, shrink move),
# then polish in high precision: python3 how-we-built-it/mp_newton.py <relaxed.txt> object.txt
