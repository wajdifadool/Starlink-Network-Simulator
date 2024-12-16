import unittest
from models.ground_control import  GroundControl

class TestGRoundControl(unittest.TestCase):
    def setUp(self):
        self.gc = GroundControl()

    def test_sats_raw(self):
        print("test_sats_raw()")
        self.assertIsNotNone(self.gc.sats_raw)

    def test_stas_lat_long(self):
        print("test_stas_lat_long()")

        sats_x_y = self.gc.sats_xy

        self.assertIsNotNone(sats_x_y)

    def test_sats(self):
        print("test_sats()")
        sats = self.gc.sats

        self.assertIsNotNone(sats)

    def test_gs(self):
        print("test_gs()")

        self.gc.gr_stations()

        self.assertIsNot(None)
    # def test_ground_stations_json(self):
    #     self.assertIsNotNone(self.gc.)


if __name__ == '__main__':
    unittest.main()