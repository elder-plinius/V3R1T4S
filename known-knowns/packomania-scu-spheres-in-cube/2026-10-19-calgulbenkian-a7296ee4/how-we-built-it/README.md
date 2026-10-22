# How we built it (scu, N = 739)

Code: `scu_attack.c` (copied from the contributor's snapshot; nothing changed except that no absolute paths occur). It reads a posted Packomania packing, deletes spheres, runs a penalty L-BFGS (`lbfgs_wall_pair`) at a target radius, then inflates the packing step by step (`inflate_packing`) and writes the coordinates with 20 decimals (`save_win`).

How the object for N = 739 was made, as far as it is documented: the triage record in the claim folder states that it is the posted N = 741 packing with 2 spheres removed and relaxed (all 739 points within 1e-3 of posted points). The snapshot's `scu_attack.c` holds the same deletion plus L-BFGS routine used for N = 738, 743 and 744 (the deletion routine reads the posted N = 740 and N = 747 files for those), but the call for N = 739 itself is NOT in the snapshot version of the file (the snapshot's source has no step for N = 739; the file was evidently edited between runs). So the exact call for this object is not recorded. The program is built with a C compiler and the math library, for example:

```sh
cc -O3 -o scu_attack scu_attack.c -lm
```

(the build line is our suggestion; the snapshot does not record it). The program reads the posted coordinate files from a local `data/coords/scu/` folder (third-party Packomania data, not shipped; fetch them yourself from packomania.com).

No PREREG.md was recorded for this cell: the snapshot of the contributor's workspace holds no pre-registration for it, so none is shipped. The exact command lines of the runs are not recorded either, except where stated below.
