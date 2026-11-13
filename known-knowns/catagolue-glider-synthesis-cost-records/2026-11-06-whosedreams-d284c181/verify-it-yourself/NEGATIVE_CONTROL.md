# Manual corrupt-RLE negative control

Kit warning: could not build a corrupted copy of object/ to test the checker. The pinned kit recognizes text by filename extension and omits .rle, so its automatic mutation step does not run. The kit code was not changed.

A separate clean package copy had the first body digit changed from 2 to 1. Both the wrapper and the actual semantic checker (without its integrity gate) rejected the resulting RLE, as recorded below. The published object was not changed.

## package wrapper
exit: 1
```
object integrity mismatch
FAIL
```
## semantic checker without integrity gate
exit: 1
```
result: {'ok': False, 'target': 'xs28_69a4owgzxol5d1d96', 'error': 'generation-0 component of 5 cells is not a glider'}
FAIL
```
