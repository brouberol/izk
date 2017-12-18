from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError


class ExtendedKazooClient(KazooClient):

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_node(self, node_path):
        """Return the JSON-deserialized content of a Zookeeper znode.

        If the node is not found, return None.

        """
        try:
            data, _ = self.get(node_path)
        except NoNodeError:
            return None
        else:
            data = data.decode('utf-8')
            return data
