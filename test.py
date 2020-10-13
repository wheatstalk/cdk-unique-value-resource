from unittest.loader import TestLoader
from unittest.runner import TextTestRunner
import os
import logging

if __name__ == "__main__":
    logging.disable()

    os.environ['PYNAMODB_CONFIG'] = os.path.join(os.path.dirname(__file__), 'py', 'localstack_pynamodb_config.py')
    os.environ['AWS_ACCESS_KEY_ID'] = 'invalid'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'invalid'

    suite = TestLoader().discover('.')
    TextTestRunner().run(suite)
