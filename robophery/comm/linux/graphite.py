import socket
import time
from robophery.comm.graphite import GraphiteCarbonComm


class LinuxGraphiteCarbonComm(GraphiteCarbonComm):

    def __init__(self, *args, **kwargs):
        self._host = kwargs.get('host', 'localhost')
        self._port = kwargs.get('port', 8125)
        self._manager = kwargs.get('manager', None)
        self._prefix = kwargs.get('prefix', self._manager._name)
        super(LinuxGraphiteCarbonComm, self).__init__(*args, **kwargs)

    def send_datum(self, datum):
        message = []
        log_message = {}
        current_time = int(time.time())
        for name, value in datum.items():
            for value_name, value_value in value.items():
                bucket = "{0}.{1}.{2}".format(self._prefix, name, value_name)
                message.append("{0} {1} {2}".format(bucket, value_value, current_time))
                log_message[bucket] = value_value
        self._log.debug("Published buckets {0} to {1}.".format(log_message, self._host))
        sock = socket.socket()
        sock.connect((self._host, self._port))
        message_string = '\n'.join(message) + '\n'
        sock.sendall(message_string)
        sock.close()
