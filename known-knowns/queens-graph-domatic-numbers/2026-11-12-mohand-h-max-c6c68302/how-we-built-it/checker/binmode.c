/* Added by the workspace, not part of drat-trim: make every fopen() of the program binary by default on Windows
   (C runtime switch set before main), so that binary DRAT proofs are not mangled by text-mode translation. */
#include <fcntl.h>
#include <stdlib.h>
__attribute__((constructor)) static void workspace_binary_mode(void) { _set_fmode(_O_BINARY); }
