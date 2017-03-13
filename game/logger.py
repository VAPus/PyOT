from time import asctime
from os import fsync

# Open files
files = {}
try:
    files["debugs"] = open("logs/debugs.log", "a")
except:
    pass
def writeEntry(file, data, producer="UNKNOWN", extra=""):
    global files
    if file not in files:
        files[file] = open("logs/%s.log" % file, "a")

    producer = "%s: By %s - %s" % (file.upper(), producer, asctime())
    if extra:
        producer += "[%s]" % extra
    files[file].write("%s:\n%s\n\n" % (producer, data))
    files[file].flush()
    fsync(files[file].fileno())