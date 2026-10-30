# Run It Yourself

From this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line:
```
PASS
```

To re-run the full compiled Rust verification engine from source:
```sh
cd how-we-built-it/code
cargo run --release --bin verify_certificates
```
