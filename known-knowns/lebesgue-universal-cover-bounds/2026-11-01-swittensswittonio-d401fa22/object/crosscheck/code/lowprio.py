import ctypes, os
def set_below_normal():
    k=ctypes.windll.kernel32; k.SetPriorityClass(k.GetCurrentProcess(),0x4000)
    return os.getpid()
