import sys, signal
import time
sys.path.insert(0, '.')
sys.path.insert(1, 'game')

# Check for good enough Python version. Use builtin path.
# XXX: Should be killed before release.
if '__pypy__' in sys.builtin_module_names:
    sys.path.insert(2, "/usr/local/lib/python3.4/dist-packages")

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
    except ImportError:
        print("Cython failed")
        pass # No cython / old cython

# Fix log machinery by replacing tornado.concurrent.
# XXX: This might be tornado 4 specific. Be aware of bugs.
import game.hack_concurrent
#del sys.modules['tornado.concurrent']
sys.modules['tornado.concurrent'] = game.hack_concurrent

#### Import the tornado ####
from tornado.tcpserver import *
import tornado.gen
from service.gameserver import GameFactory
import time
import game.loading
import tornado.log
tornado.log.enable_pretty_logging()

startTime = time.time()
# Game Server
gameServer = GameFactory()
gameServer.bind(config.gamePort, config.gameInterface)
gameServer.start()

# (optionally) buildt in login server.
if config.letGameServerRunTheLoginServer:
    from service.loginserver import LoginFactory
    loginServer= LoginFactory()
    loginServer.bind(config.loginPort, config.loginInterface)
    loginServer.start()
    
# (optional) built in extension server.
# XXX Port later or kill?
#if config.enableExtensionProtocol:
#    from service.extserver import ExtFactory
#    extFactory = ExtFactory()
#    tcpService = internet.TCPServer(config.loginPort + 10000, extFactory, interface=config.loginInterface)
#    tcpService.setServiceParent(topService)

# (optional) built in extension server.
# XXX: Port later...
if config.enableWebProtocol:
    from service.webserver import Web
    from tornado import httpserver
    webServer = tornado.httpserver.HTTPServer(Web)
    webServer.bind(config.webPort, config.webInterface)
    webServer.start()


# Load the core stuff!
IOLoop.instance().add_callback(game.loading.loader, startTime)

# Start reactor. This will call the above.
signal.signal(signal.SIGINT, game.scriptsystem.shutdown)
signal.signal(signal.SIGTERM, game.scriptsystem.shutdown)
IOLoop.instance().start()

