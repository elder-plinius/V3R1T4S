from pathlib import Path
from hashlib import sha256
EXPECTED = {'PROOF.md': '6c01be8056dce86ca1cef0df2df38c99b1747e463bc1069c6c4e0a3fcf915837', 'algebraic-core-direct.json': 'fb35ba0b080114cd41f7b8685e1d3f5813c51d081e7986cfe4c07d60823082fe'}
for name,digest in EXPECTED.items():
 assert sha256((Path("object")/name).read_bytes()).hexdigest()==digest, "reviewed object changed: "+name
print("reviewed object identity: PASS (hash binding only)")
