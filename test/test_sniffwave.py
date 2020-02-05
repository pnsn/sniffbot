from sniffbot.models import SniffWave
import unittest


class TestReadLog(unittest.TestCase):
    s = SniffWave('RCM', None, None, None, 5)
    r = s.parse_log()
    print(r)
