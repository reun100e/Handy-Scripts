import unittest
from datetime import datetime
from organize_by_date import get_photo_date, get_video_date, organize_files_by_date
import os
import shutil


class TestDateParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs("test_files/test_images", exist_ok=True)
        os.makedirs("test_files/test_videos", exist_ok=True)
        os.makedirs("test_files/test_images/subdir", exist_ok=True)
        os.makedirs("test_files/test_videos/subdir", exist_ok=True)

        # Create test files with known dates
        cls.test_image_path = "test_files/test_images/test_image.jpg"
        cls.test_video_path = "test_files/test_videos/test_video.mp4"
        cls.test_image_subdir_path = "test_files/test_images/subdir/test_image.jpg"
        cls.test_video_subdir_path = "test_files/test_videos/subdir/test_video.mp4"

        # Add some mock content
        with open(cls.test_image_path, "w") as f:
            f.write("test")
        with open(cls.test_video_path, "w") as f:
            f.write("test")
        with open(cls.test_image_subdir_path, "w") as f:
            f.write("test")
        with open(cls.test_video_subdir_path, "w") as f:
            f.write("test")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("test_files")

    def test_get_photo_date(self):
        expected_date = datetime(2022, 12, 7, 1, 46, 35)
        self.assertEqual(get_photo_date(self.test_image_path), expected_date)

    def test_get_video_date(self):
        expected_date = datetime(2022, 12, 7, 1, 46, 35)
        self.assertEqual(get_video_date(self.test_video_path), expected_date)

    def test_get_video_date_alternative_format(self):
        expected_date = datetime(2022, 12, 7, 1, 46, 35)
        self.assertEqual(get_video_date(self.test_video_path), expected_date)

    def test_photo_date_missing_exif(self):
        self.assertIsNone(get_photo_date(self.test_image_path))

    def test_video_date_missing_metadata(self):
        self.assertIsNone(get_video_date(self.test_video_path))

    def test_files_in_subdirectories(self):
        expected_date = datetime(2022, 12, 7, 1, 46, 35)
        self.assertEqual(get_photo_date(self.test_image_subdir_path), expected_date)
        self.assertEqual(get_video_date(self.test_video_subdir_path), expected_date)


if __name__ == "__main__":
    unittest.main()
