import DeletionCode.Cert_16_2
import DeletionCode.Cert_16_2Max.B00
import DeletionCode.Cert_16_2Max.B01
import DeletionCode.Cert_16_2Max.B02
import DeletionCode.Cert_16_2Max.B03
import DeletionCode.Cert_16_2Max.B04
import DeletionCode.Cert_16_2Max.B05
import DeletionCode.Cert_16_2Max.B06
import DeletionCode.Cert_16_2Max.B07
import DeletionCode.Cert_16_2Max.B08
import DeletionCode.Cert_16_2Max.B09
import DeletionCode.Cert_16_2Max.B10
import DeletionCode.Cert_16_2Max.B11
import DeletionCode.Cert_16_2Max.B12
import DeletionCode.Cert_16_2Max.B13
import DeletionCode.Cert_16_2Max.B14
import DeletionCode.Cert_16_2Max.B15
import DeletionCode.Cert_16_2Max.B16
import DeletionCode.Cert_16_2Max.B17
import DeletionCode.Cert_16_2Max.B18
import DeletionCode.Cert_16_2Max.B19
import DeletionCode.Cert_16_2Max.B20
import DeletionCode.Cert_16_2Max.B21
import DeletionCode.Cert_16_2Max.B22
import DeletionCode.Cert_16_2Max.B23
import DeletionCode.Cert_16_2Max.B24
import DeletionCode.Cert_16_2Max.B25
import DeletionCode.Cert_16_2Max.B26
import DeletionCode.Cert_16_2Max.B27
import DeletionCode.Cert_16_2Max.B28
import DeletionCode.Cert_16_2Max.B29
import DeletionCode.Cert_16_2Max.B30
import DeletionCode.Cert_16_2Max.B31

namespace DeletionCode.Cert_16_2

/-- Pure-kernel Inclusion-Maximality (Non-Extendability) Certificate over ALL 2^16 = 65536 binary words.
    NOTE (-0 Hype): Proves no single word can be added to `code`; does NOT claim global optimality M_2(16) <= 219. -/
theorem inclusion_maximal : IsInclusionMaximal 16 2 code :=
  inclusionMaximal_of_blocks (b := 5) (d := 11) rfl fun blk hblk y hy =>
    match blk, hblk with
    | 0, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 0 Cert_16_2Max.tree_0 Cert_16_2Max.ok_0 y hy
    | 1, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 1 Cert_16_2Max.tree_1 Cert_16_2Max.ok_1 y hy
    | 2, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 2 Cert_16_2Max.tree_2 Cert_16_2Max.ok_2 y hy
    | 3, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 3 Cert_16_2Max.tree_3 Cert_16_2Max.ok_3 y hy
    | 4, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 4 Cert_16_2Max.tree_4 Cert_16_2Max.ok_4 y hy
    | 5, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 5 Cert_16_2Max.tree_5 Cert_16_2Max.ok_5 y hy
    | 6, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 6 Cert_16_2Max.tree_6 Cert_16_2Max.ok_6 y hy
    | 7, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 7 Cert_16_2Max.tree_7 Cert_16_2Max.ok_7 y hy
    | 8, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 8 Cert_16_2Max.tree_8 Cert_16_2Max.ok_8 y hy
    | 9, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 9 Cert_16_2Max.tree_9 Cert_16_2Max.ok_9 y hy
    | 10, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 10 Cert_16_2Max.tree_10 Cert_16_2Max.ok_10 y hy
    | 11, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 11 Cert_16_2Max.tree_11 Cert_16_2Max.ok_11 y hy
    | 12, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 12 Cert_16_2Max.tree_12 Cert_16_2Max.ok_12 y hy
    | 13, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 13 Cert_16_2Max.tree_13 Cert_16_2Max.ok_13 y hy
    | 14, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 14 Cert_16_2Max.tree_14 Cert_16_2Max.ok_14 y hy
    | 15, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 15 Cert_16_2Max.tree_15 Cert_16_2Max.ok_15 y hy
    | 16, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 16 Cert_16_2Max.tree_16 Cert_16_2Max.ok_16 y hy
    | 17, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 17 Cert_16_2Max.tree_17 Cert_16_2Max.ok_17 y hy
    | 18, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 18 Cert_16_2Max.tree_18 Cert_16_2Max.ok_18 y hy
    | 19, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 19 Cert_16_2Max.tree_19 Cert_16_2Max.ok_19 y hy
    | 20, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 20 Cert_16_2Max.tree_20 Cert_16_2Max.ok_20 y hy
    | 21, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 21 Cert_16_2Max.tree_21 Cert_16_2Max.ok_21 y hy
    | 22, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 22 Cert_16_2Max.tree_22 Cert_16_2Max.ok_22 y hy
    | 23, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 23 Cert_16_2Max.tree_23 Cert_16_2Max.ok_23 y hy
    | 24, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 24 Cert_16_2Max.tree_24 Cert_16_2Max.ok_24 y hy
    | 25, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 25 Cert_16_2Max.tree_25 Cert_16_2Max.ok_25 y hy
    | 26, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 26 Cert_16_2Max.tree_26 Cert_16_2Max.ok_26 y hy
    | 27, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 27 Cert_16_2Max.tree_27 Cert_16_2Max.ok_27 y hy
    | 28, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 28 Cert_16_2Max.tree_28 Cert_16_2Max.ok_28 y hy
    | 29, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 29 Cert_16_2Max.tree_29 Cert_16_2Max.ok_29 y hy
    | 30, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 30 Cert_16_2Max.tree_30 Cert_16_2Max.ok_30 y hy
    | 31, _ => checkMax2_block Cert_16_2.codeTrie_ok 11 31 Cert_16_2Max.tree_31 Cert_16_2Max.ok_31 y hy
    | _ + 32, hlt => absurd hlt (by omega)

end DeletionCode.Cert_16_2
