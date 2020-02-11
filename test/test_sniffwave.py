from sniffbot.models import SniffWave
import unittest


class TestSniffWave(unittest.TestCase):
    def setUp(self):
        self.intro = \
            'test1 Sniffing WAVE_RING for JCW.wild.wild.wild\n'
        self.scnl = "JCW.EHZ.UW.-- (0x32 0x30) 0 i4  73 100.0 2020/02/02\n"\
            "23:40:41.80 (1580686841.8000) 2020/02/02 23:40:42.52\n"\
            "(1580686842.5200) 0x00 0x00 i2 m72 t19 len 356\n"\
            "[D: 3.0s F: 0.0s]"
        self.summary = "Sniffed WAVE_RING for 10 seconds:\n" \
            "\tStart Time of first packet:  2020/02/10 20:59:59.97\n" \
            "\t\tEnd Time of last packet:  2020/02/10 21:00:01.96\n" \
            "\t\t\tSeconds of data:  1.990002\n" \
            "\t\t\t\tBytes of data:  3980\n" \
            "\tNumber of Packets of data:  19\n"
        self.summary_no_data = \
            'Sniffed WAVE_RING for 5 seconds and found no packets matching '\
            'desired SCN[L] filter .'

    def test_sms_text_formating(self):
        s = SniffWave('RCM', None, None, None)
        
        res = s.parse_message(self.intro)
        self.assertEqual(res, ["Sniffing WAVE_RING",
                               " for JCW.wild.wild.wild"])
        res = s.parse_message(self.scnl)
        self.assertEqual(res,
                         ["CW.EHZ.UW.-- 73 100.0 2020/02/02 23:40:41.80",
                          "2020/02/02 23:40:42.52 356 [D: 3.0s F: 0.0s]"])
