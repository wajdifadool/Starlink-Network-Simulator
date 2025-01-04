import unittest
from models.file_manager import  FileManager

class TestLoadingFiles(unittest.TestCase):
    def setUp(self):
        self.fm = FileManager()

    def test_load_stas_file(self):
        print("test_load_stas_file")
        self.assertIsNotNone(self.fm.load_tle_file_into_list())
        #
    def test_loadig_ground_stations_file(self):
        print("test_loadig_ground_stations_file")

        self.assertIsNotNone(self.fm.load_ground_stations())

if __name__ == '__main__':
    pass
    # unittest.main()