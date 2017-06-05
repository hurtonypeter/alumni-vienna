from zqfa.worker.worker import conn, Connection, Queue, listen, Worker

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

