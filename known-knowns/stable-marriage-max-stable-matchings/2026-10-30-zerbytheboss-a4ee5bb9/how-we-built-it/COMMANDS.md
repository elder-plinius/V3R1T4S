# Commands used to build and find the object

```sh
# 1. Compile the search and counting engine
cc -O3 -o smcount3 smcount3.c -lm

# 2. Run adaptive kick-step hill climbing seeded from Thurber's G17 matrix
# (G17 is the 17x17 submatrix of bitwise XOR i ^ j)
./smcount3 climb 17 g_17.prefs 99999 60 climb17 1500 2
```

At evaluation 2,302, the search produced `climb17.best.prefs` with 206,728 stable matchings.
This profile was preserved as `object/instance_n17.txt`.
