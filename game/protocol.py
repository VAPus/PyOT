import sys, os, glob, importlib

protocolsAvailable = []
for path in glob.iglob('game/protocols/*.py'):
    version = path.split(os.sep)[-1].split('.', 1)[0]
    if not '_' in version and not '.' in version and not 'base' in version:
        protocolsAvailable.append(int(version))

protocolsUsed = {}

def getProtocol(version):
    if not protocolsUsed:
        loadProtocol(version)
    try:
        return protocolsUsed[version]
    except:
        print("Protocol %d unsupported" % version)
    return None

def loadProtocol(version):
    if "_trial_temp" in os.getcwd():
        os.chdir("..")

    if not version in protocolsAvailable:
        print("Protocol (Base) %d doesn't exist!" % version)
        return

    protocol = importlib.import_module('game.protocols.%d' % version)

    protocol.verify()
    protocolsUsed[version] = protocol.Protocol()
    for x in protocol.provide:
        protocolsUsed[x] = protocolsUsed[version]
