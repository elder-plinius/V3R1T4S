# Deterministic Recipe & SHA-256 Digests for Tokenized Test Texts (`frozen_test_tensors_seed42.npz` & `bert_test_strict_1875.txt`)

To avoid redistributing the tokenized Oracc test texts (`1,875` texts $\times 128$ tokens) inside `object/`, `frozen_test_tensors_seed42.npz` is replaced by this deterministic regeneration recipe from the upstream `SLAB-NLP/Akk` repository (`https://github.com/SLAB-NLP/Akk`, commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`).

## 1. Upstream & Generated File SHA-256 Digests

| File | Byte Size | SHA-256 Digest |
|---|---:|---|
| Upstream `SLAB-NLP/Akk`: `data/akk_from_jsons.jsonl` | `21,156,545` | `b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3` |
| Deduplicated held-out test lines: `bert_test_strict_1875.txt` | `1,256,550` | `65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c` |
| Tokenized & masked test tensors (`seed = 42`): `frozen_test_tensors_seed42.npz` | `302,914` | `8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4` |
| Frozen masked position coordinate manifest: `frozen_masked_positions.json` | `5,780,131` | `4abcfdb61d6a391d07b024136ace51d4dc4e3378a7ad2b89b6b12e1de75216c1` |

## 2. Exact Regeneration Script (`SLAB-NLP/Akk` at Commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`)

1. Run `preprocessing/main_preprocess.py` (`SEED = 2`, 80/20 split on `data/akk_from_jsons.jsonl`) to produce `akk_train.jsonl` (`18,568` rows) and `akk_test.jsonl` (`4,643` rows), and filter `akk_test.jsonl` as in `akkadian_bert/main_bert.py` (lines 160–180) to remove all `id_text` values present in `akk_train.jsonl` plus empty/duplicate `bert_input` lines, yielding `bert_test_strict_1875.txt` (`1,875` lines, `1,256,550` bytes, `sha256: 65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c`).
2. Tokenize and apply `DataCollatorForLanguageModelingAkkadian` at `torch.manual_seed(42)`:

```python
import hashlib
import numpy as np
import torch
from transformers import BertTokenizerFast
from akkadian_bert.datasets_bert import ORACCDataset
from akkadian_bert.data_collators_bert import DataCollatorForLanguageModelingAkkadian

tok = BertTokenizerFast.from_pretrained("main_tokenizer")
tok._pad_token = tok.pad_token
ds = ORACCDataset(
    file_path="bert_test_strict_1875.txt",
    tokenizer=tok,
    block_size=128,
    missing_sign_encoding=tok.get_vocab()["x"],
    encode_only_first_token_in_word=False,
    ignore_missing=True,
)
collator = DataCollatorForLanguageModelingAkkadian(tokenizer=tok, mlm_probability=0.15, missing_sign="x")
torch.manual_seed(42)
batch = collator([ds[i] for i in range(len(ds))])
np.savez_compressed(
    "frozen_test_tensors_seed42.npz",
    input_ids=batch["input_ids"].numpy(),
    labels=batch["labels"].numpy(),
)
assert hashlib.sha256(open("frozen_test_tensors_seed42.npz", "rb").read()).hexdigest() == (
    "8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4"
)
```
