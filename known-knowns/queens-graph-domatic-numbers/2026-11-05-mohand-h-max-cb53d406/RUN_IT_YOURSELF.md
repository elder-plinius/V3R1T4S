# Run it yourself

From this folder, in a fresh shell with Python 3 (standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output ends with `PASS`. The script checks the sha256 of object/dom-Q11-19-partition.txt (cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4; the file has
CRLF line endings; if a checkout converts them to LF, the content is identical and its sha256 is
3beb06dc4cb19d7e3e5f690deaf36bf54d222d7ebd62a1eb541dbf25f160e78e, which is also accepted), then checks from the definition that the 11 x 11
grid uses 19 labels and that every class dominates the queens graph Q_11.

To rebuild the object, see how-we-built-it/COMMANDS.md (C# on .NET Framework 4.x, Python 3 with numpy and scipy).
