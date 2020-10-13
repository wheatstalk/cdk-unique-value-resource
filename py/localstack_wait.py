from datetime import datetime, timedelta
import logging
import time

from pynamodb.connection import Connection
from pynamodb.exceptions import TableError


def wait():
    connection = Connection(host="http://localhost:4566")

    timeout = datetime.now() + timedelta(seconds=60)
    while datetime.now() < timeout:
        try:
            connection.list_tables()
            logging.info(f'Localstack is ready')
            return
        except TableError as e:
            logging.info(f'Localstack is not ready')
            time.sleep(5)

    raise Exception('Timed out')


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    wait()
