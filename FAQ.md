# The server have high CPU load for one/few requests
* The server use a reactor design, polling technics is by far the heaviest load, but the load is mostly in the kernel. One user (running at maximum speed, server sending), this does NOT scale linearly (monsters doesn't think twice just because there is two players in the area etc), it takes cPython about 0.3-0.7% (of a 1600Mhz clocked i7-3770 core), while 30 takes about 5%.
  This evens out.
  See: http://monkey.org/~provos/libevent/libevent-benchmark.jpg

# Unloading does not free memory
* Deleting memory /freeing in Python does not release the memory to the operating system. It's reused internally.

# We assume without additional performance hacks, the server could scale to handle about 1000 players using CPython, on a i7-3770 system.
