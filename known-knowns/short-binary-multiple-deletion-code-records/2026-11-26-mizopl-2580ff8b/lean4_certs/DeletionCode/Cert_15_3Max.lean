import DeletionCode.Cert_15_3
import DeletionCode.Cert_15_3Max.B00
import DeletionCode.Cert_15_3Max.B01
import DeletionCode.Cert_15_3Max.B02
import DeletionCode.Cert_15_3Max.B03
import DeletionCode.Cert_15_3Max.B04
import DeletionCode.Cert_15_3Max.B05
import DeletionCode.Cert_15_3Max.B06
import DeletionCode.Cert_15_3Max.B07
import DeletionCode.Cert_15_3Max.B08
import DeletionCode.Cert_15_3Max.B09
import DeletionCode.Cert_15_3Max.B10
import DeletionCode.Cert_15_3Max.B11
import DeletionCode.Cert_15_3Max.B12
import DeletionCode.Cert_15_3Max.B13
import DeletionCode.Cert_15_3Max.B14
import DeletionCode.Cert_15_3Max.B15

namespace DeletionCode.Cert_15_3

/-- Pure-kernel Inclusion-Maximality (Non-Extendability) Certificate over ALL 2^15 = 32768 binary words.
    NOTE (-0 Hype): Proves no single word can be added to `code`; does NOT claim global optimality M_3(15) <= 31. -/
theorem inclusion_maximal : IsInclusionMaximal 15 3 code :=
  inclusionMaximal_of_blocks (b := 4) (d := 11) rfl fun blk hblk y hy =>
    match blk, hblk with
    | 0, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 0 Cert_15_3Max.tree_0 Cert_15_3Max.ok_0 y hy
    | 1, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 1 Cert_15_3Max.tree_1 Cert_15_3Max.ok_1 y hy
    | 2, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 2 Cert_15_3Max.tree_2 Cert_15_3Max.ok_2 y hy
    | 3, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 3 Cert_15_3Max.tree_3 Cert_15_3Max.ok_3 y hy
    | 4, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 4 Cert_15_3Max.tree_4 Cert_15_3Max.ok_4 y hy
    | 5, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 5 Cert_15_3Max.tree_5 Cert_15_3Max.ok_5 y hy
    | 6, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 6 Cert_15_3Max.tree_6 Cert_15_3Max.ok_6 y hy
    | 7, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 7 Cert_15_3Max.tree_7 Cert_15_3Max.ok_7 y hy
    | 8, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 8 Cert_15_3Max.tree_8 Cert_15_3Max.ok_8 y hy
    | 9, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 9 Cert_15_3Max.tree_9 Cert_15_3Max.ok_9 y hy
    | 10, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 10 Cert_15_3Max.tree_10 Cert_15_3Max.ok_10 y hy
    | 11, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 11 Cert_15_3Max.tree_11 Cert_15_3Max.ok_11 y hy
    | 12, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 12 Cert_15_3Max.tree_12 Cert_15_3Max.ok_12 y hy
    | 13, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 13 Cert_15_3Max.tree_13 Cert_15_3Max.ok_13 y hy
    | 14, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 14 Cert_15_3Max.tree_14 Cert_15_3Max.ok_14 y hy
    | 15, _ => checkMax3_block Cert_15_3.codeTrie_ok 11 15 Cert_15_3Max.tree_15 Cert_15_3Max.ok_15 y hy
    | _ + 16, hlt => absurd hlt (by omega)

end DeletionCode.Cert_15_3
