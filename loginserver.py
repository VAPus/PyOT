import sys
sys.path.insert(0, '.')
sys.path.insert(1, 'game')

try:
    import config
except ImportError:
    print("You got no config.py file. Please make a file from config.py.dist")
    sys.exit()

#### Try Cython? ####
if config.tryCython:
    try:
        import pyximport
        pyximport.install(pyimport = True)
    except:
        pass # No cython / old cython

# Fix log machinery by replacing tornado.concurrent.
# XXX: This might be tornado 4 specific. Be aware of bugs.
import game.hack_concurrent
#del sys.modules['tornado.concurrent']
sys.modules['tornado.concurrent'] = game.hack_concurrent

#### Import the tornado ####
from tornado.tcpserver import *
from tornado.ioloop import IOLoop
    
from service.loginserver import LoginFactory
loginServer= LoginFactory()
loginServer.bind(config.loginPort, config.loginInterface)
loginServer.start()

# Start reactor. This will call the above.
IOLoop.instance().start()
            
