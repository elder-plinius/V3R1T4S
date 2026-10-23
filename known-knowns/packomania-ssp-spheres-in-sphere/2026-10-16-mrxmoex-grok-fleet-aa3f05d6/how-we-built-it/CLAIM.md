# Claim (skeptic view; nothing else)
Packomania ssp (N equal spheres in a sphere of radius 1, centered at origin). For each N in the N column of object/ssp_radiustxt_errata.csv (90 values, 1055..50000):
the value in https://packomania.com/ssp/txt/radius.txt exceeds by more than 1e-10 the feasible radius
r* = min( min_{i<j}|c_i-c_j|/2 , 1 - max_i |c_i| ) of the posted coordinates (ssp<N>.txt inside https://packomania.com/ssp/txt/ssp_coords.tar.gz),
while the radius shown in https://packomania.com/ssp/ssp.html for the same N agrees with r* within 1e-10 (observed <= 2.8e-12).
Gaps (r* - radius.txt) range from about -6.09e-9 (N=1601) to -6.48e-5 (N=20000). Container radius 1; tables have 12 decimals. In short: the posted coordinates (and ssp.html) do not certify the radius.txt value.
