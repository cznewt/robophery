
import logging

class Module(object):

    def __init__(self):
       self._logger = logging.getLogger("robophery")


    def publish_data(self):
        pass
        #mqtt publish


    def service_loop(self):

        while True:
            self.read_data
            sleep(1000)

