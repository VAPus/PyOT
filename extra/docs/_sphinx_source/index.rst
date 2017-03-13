****************************
  What's PyOT
****************************

:Author: Stian (:vapus:`members/stian`)
:Release: |release|
:Date: |today|

PyOT is a server written in Python, using that Twisted framework that emulates the Tibia protocol.

PyOT is super fast, and uses diffrent methods than other projects. Some of which is:

* Async SQL
* Async core code
* Async scriptsystem
* Ability to utilize the best reactor designs (epoll (Linux), iocp (Windows) and kqueue (FreeBSD))
* Ability to utilize JIT using PyPy
* Very flexible core
* Very configurable core
* Very fast save format (save takes from less than 0.1ms to 0.3ms per player, scales over several sql connections, allowing for upto 10k saves per second)
* Sector maps, dynamic load and unload for optimal memory usage (down to ~50MB on 64bit after login! (32bit can expect around half)) (*Multilingual mode may require more) 
* Support for instances or even having multiple worlds on one server!
* Support for multiple languages (at the same time, now each individual account can have their own language!) (*all server sided messages, client UI is a different matter)
* Ability to dynamicly script maps and custom items!

Ideas (not yet desided):

* Support for own Status protocol
* Support for dynamic upgrade of custom clients over a custom protocol (useful for say, autoupdaters)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 2

   modules
   scriptevents
   tfsToPyOT
