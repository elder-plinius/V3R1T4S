# Run it yourself

From this folder, in a fresh shell with Python 3 (standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output ends with `PASS`. The script checks the sha256 of object/dom-Q12-21-partition.txt (e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e; the file has
CRLF line endings, and a copy converted to LF hashes differently), then checks from the definition that the 12 x 12
grid uses 21 labels and that every class dominates the queens graph Q_12.

To rebuild the object, see how-we-built-it/COMMANDS.md (C# on .NET Framework 4.x; about two minutes on one thread).
