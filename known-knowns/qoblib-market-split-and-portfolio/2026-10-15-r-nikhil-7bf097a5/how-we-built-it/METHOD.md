# Search implementation and rerun

The supplied code is the actual discovery implementation. It requires Python with NumPy 2.0.2; the verifier does not. No claim depends on heuristic timing or rediscovery of an identical final trajectory.

With the hash-checked public inputs saved as `stock_prices.txt.gz` and `covariance_matrices.txt.gz` under an `INSTANCE` directory, these concrete commands rerun the component searches (replace INSTANCE with that directory):

```sh
python3 how-we-built-it/code/beam_exchange_distinct.py INSTANCE how-we-built-it/seed.sol work/distinct 2100 1426
python3 how-we-built-it/code/long_periods.py INSTANCE work/distinct/best.sol work/periods 1800 1427
python3 how-we-built-it/code/block_beam.py INSTANCE work/periods/best.sol work/blocks 1800 1428
python3 how-we-built-it/code/net_beam.py INSTANCE work/blocks/best.sol work/net 1380 1429
```

These seeds specify a fresh rerun, not an asserted reconstruction of undocumented historical random streams. Set numerical thread limits to one and cap the overall job. The historical final recombination selected period rows from multiple live search pools; the verified resulting coordinates are saved in object/portfolio.sol. The exact discovery-time objectives and component methods are documented in HOW_WE_FOUND_IT.md.
