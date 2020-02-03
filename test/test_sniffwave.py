from sniffbot.models import SniffWave
import unittest


class TestSniffWave(unittest.TestCase):
    def test_sms_text_formating(self):
        s = SniffWave('RCM', None, None, None)
        intro = 'Sniffing WAVE_RING for JCW.wild.wild.wild'
        scnl = "JCW.EHZ.UW.-- (0x32 0x30) 0 i4  73 100.0 2020/02/02 "\
               "23:40:41.80 (1580686841.8000) 2020/02/02 23:40:42.52 "\
               "(1580686842.5200) 0x00 0x00 i2 m72 t19 len 356 "\
               "[D: 3.0s F: 0.0s]"
        res = s.parse_message(intro)
        self.assertEqual(res, ["Sniffing WAVE_RING",
                               " for JCW.wild.wild.wild"])
        res = s.parse_message(scnl)
        self.assertEqual(res,
                         ["CW.EHZ.UW.-- 73 100.0 2020/02/02 23:40:41.80",
                          "2020/02/02 23:40:42.52 356 [D: 3.0s F: 0.0s]"])
