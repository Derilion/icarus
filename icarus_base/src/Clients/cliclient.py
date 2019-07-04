from src.Clients.superclient import SuperClient, ClientStopException


class CLIClient(SuperClient):

    def run(self):
        while not self.stop_request:
            try:
                a = input("# ")
                self._queue_new_message(a)
                print("Thread with id " + str(self.id) + " doesn't care")
            except ClientStopException:
                print("gotcha")
                break

    def send(self, message: str, client_attr):
        print(message)

    def stop(self):
        print("stopping thread with id " + str(self.id))
        del self
        raise ClientStopException("Stopping Thread")
