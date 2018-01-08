from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, ConnectionLoss


class ExtendedKazooClient(KazooClient):

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def command(self, cmd='ruok'):
        """Sends a commmand to the ZK node.

        Overrides methode defined at
        https://github.com/python-zk/kazoo/blob/release/2.4/kazoo/client.py#L637
        as it could leave some data unread from the socket.

        """
        if not self._live.is_set():
            raise ConnectionLoss("No connection to server")
        out = []
        peer = self._connection._socket.getpeername()
        if len(peer) > 2:
            peer = peer[:2]
        sock = self.handler.create_connection(
            peer, timeout=self._session_timeout / 1000.0)
        sock.sendall(cmd)
        while True:
            data = sock.recv(8192)
            if not data:
                break
            out.append(data)

        sock.close()
        result = b''.join(out)
        return result.decode('utf-8', 'replace')

    def stat(self, node_path):
        try:
            _, stat = self.get(node_path)
        except NoNodeError:
            return None
        else:
            return stat
