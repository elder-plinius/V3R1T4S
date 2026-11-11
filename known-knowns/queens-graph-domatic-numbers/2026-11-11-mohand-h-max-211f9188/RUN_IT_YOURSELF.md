# Run it yourself

From this folder, in a fresh shell with Python 3 (standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output ends with `PASS`. The script checks the sha256 of object/tdom-Q10-16-partition.txt (211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec; the file has
CRLF line endings, and a copy converted to LF hashes differently), then checks from the definition that the 10 x 10
grid uses 16 labels and that every class totally dominates the queens graph Q_10 (every square, members included, is
attacked by another member of the class).

To rebuild the object, see how-we-built-it/COMMANDS.md (C# on .NET Framework 4.x; about one minute on one thread).
