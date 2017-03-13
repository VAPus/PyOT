from tornado import gen

# A test frontpage.

@registerWeb(r'/')
class Frontpage(RequestHandler):
    def get(self):
        self.write("This is the frontpage")
        self.finish()


# More effective design.
@registerWeb(r'/delay')
class SQL(RequestHandler):
    @gen.coroutine
    def get(self):
        self.write("Sleeping...") # Send
        self.flush() # Send text
        yield gen.Task(ioloop_ins.add_timeout, time.time() + 5) # Sleep for 5 seconds
        self.write("<html><body>Sorry to keep you waiting.</body></html>") # Send body
        self.finish() # Finish request
