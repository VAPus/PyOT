In order to run PyOT you need:
================================

* Python 3.4+ or (pypy currently NOT supported until they get python 3.4 support ATM on 3.2)

* Tornado 4+

* pymysql

* Optional: pywin32 may give a better eventloop on windows

* Optional: cffi enable some C extension for better performance.

Links for Windows:
------------------

https://www.python.org/ftp/python/3.4.1/python-3.4.1.amd64.msi

http://www.lfd.uci.edu/~gohlke/pythonlibs/#tornado (tornado-4.0.2-win-amd64-py3.4.exe)

=======

Open cmd and run:
c:\Python34\Scripts\easy_install.exe pymysql

Optional:
http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download



Installation
============

Copy "config.py.dist" to "config.py" and edit it to match your database settings.

Run gameserver.py, it will automatically set up your database :)

Linux (any distro)
---------------------------------------------

Install python3.3+ from package management. You may loop for tornado4 and pymysql there as well.
Otherwise:

pip install tornado
pip install pymysql

or

pip3 install tornado
pip3 install pymysql 


Documentation
=============

You can find additional documentation of PyOT here: http://vapus.net/pyot_doc/index.html

Useful scripting guide here: http://vapus.net/pyot_doc/scriptevents.html
