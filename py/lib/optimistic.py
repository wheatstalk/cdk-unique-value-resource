import logging

import os
import time
import random
from pynamodb.exceptions import PutError, TransactGetError, TransactWriteError

retry_codes = [
    'ConditionalCheckFailedException', 'ThrottlingException', 'RequestLimitExceeded',
    'ProvisionedThroughputExceededException', 'LimitExceededException', 'ItemCollectionSizeLimitExceededException',
    'TransactionCanceledException'
]
sleep_coefficient = 1 if 'AWS_REGION' in os.environ else 0
retries = 600


def check_for_retry_code(e):
    if e.cause_response_code in retry_codes:
        if sleep_coefficient > 0:
            time.sleep(random.random() * sleep_coefficient)
        return
    else:
        logging.error(f'Non-retry error: {e.cause_response_code}: {e.cause_response_message}')
        raise e


def optimistic_retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(0, retries):
            try:
                return func(*args, **kwargs)

            except TransactWriteError as e:
                check_for_retry_code(e)
            except TransactGetError as e:
                check_for_retry_code(e)
            except PutError as e:
                check_for_retry_code(e)
            except Exception as e:
                logging.error(f'Other exception: {e}')
                raise

        raise Exception('Optimistic locking ran out of attempts')

    return wrapper
