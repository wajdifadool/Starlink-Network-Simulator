import unittest
from models.ground_control import  GroundControl

class TestGRoundControl(unittest.TestCase):
    def setUp(self):
        print("TestGRoundControl--> setUp")
        self.gc = GroundControl()

    def test_sats_raw(self):
        print("TestGRoundControl--> test_sats_raw()")
        self.assertIsNotNone(self.gc.sats_raw)

    def ptest_stas_lat_long(self):
        print("TestGRoundControl--> test_stas_lat_long()")
        sats_x_y = self.gc.sats_xy

        self.assertIsNotNone(sats_x_y)

    def test_sats(self):
        print("TestGRoundControl--> test_sats()")
        sats = self.gc.sats
        self.assertIsNotNone(sats)


    def test_loading_sats_by_name(self):
        print("TestGRoundControl--> test_loading_sats_by_name()")
        by_name = self.gc.load_sats_by_name()
        self.assertIsNotNone(by_name)

    def test_sats_into_dict(self):
        print("TestGRoundControl--> test_sats_into_dict()------------------")
        by_name = self.gc.load_sats_dict_lat_long()
        self.assertIsNotNone(by_name)


if __name__ == '__main__':
    unittest.main()