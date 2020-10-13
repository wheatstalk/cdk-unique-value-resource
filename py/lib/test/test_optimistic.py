import unittest

from botocore.exceptions import ClientError
from pynamodb.exceptions import PutError

from py.lib.optimistic import optimistic_retry


class TestOptimistic(unittest.TestCase):
    def test_optimism(self):
        # GIVEN
        attempts = 0

        @optimistic_retry
        def fail():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise PutError(cause=ClientError({'Error': {'Code': 'ConditionalCheckFailedException'}}, 'PutItem'))

        # WHEN
        fail()

        # THEN
        self.assertEqual(3, attempts)

    def test_allocation_attempts(self):
        # GIVEN
        @optimistic_retry
        def fail():
            raise PutError(cause=ClientError({'Error': {'Code': 'ConditionalCheckFailedException'}}, 'PutItem'))

        # WHEN / THEN
        with self.assertRaisesRegex(Exception, r'attempts'):
            fail()

    def test_allocation_raises_other_errors(self):
        # GIVEN
        @optimistic_retry
        def fail():
            raise PutError(cause=ClientError({'Error': {'Code': 'AccessDenied'}}, 'PutItem'))

        # WHEN / THEN
        with self.assertRaises(PutError):
            fail()