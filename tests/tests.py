import unittest
from core.picture import Picture
from PIL import Image
from shutil import copyfile, rmtree
import os

class PictureTestCase(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_dir = "{}{}test_dir".format(self.current_dir, os.path.sep)
        self.base_picture = "python_image_2000_2000.png"
        os.mkdir(self.test_dir)

    def tearDown(self):
        rmtree(self.test_dir)

    def test_nonexistent_file(self):
        fake_file = "{}{}fake_file".format(self.current_dir, os.path.sep)
        p = Picture(fake_file)
        response = p.resize_picture()
        self.assertEqual(response, {"It will not change": "Not a file"})

    def test_image_2mp(self):
        # Testing picture with 2000px X 2000px
        copyfile("{}{}{}".format(self.current_dir, os.path.sep, self.base_picture), 
            "{}{}{}".format(self.test_dir, os.path.sep, self.base_picture))
        im = Image.open("{}{}{}".format(self.test_dir, os.path.sep, self.base_picture))
        width_before, height_before = im.size
        width_after, height_after = None, None
        im.close()

        p = Picture("{}{}{}".format(self.test_dir, os.path.sep, self.base_picture))
        response = p.resize_picture()
        im = Image.open("{}{}{}_resized{}".format(self.test_dir, os.path.sep,
            os.path.splitext(self.base_picture)[0], os.path.splitext(self.base_picture)[1]))
        width_after, height_after = im.size
        im.close()
        
        '''
        Selection rule: the height will have a greater difference, using the "new_height"
        method of the Dimensions class. New image size: 1920px X 1920px (square image).
        Calculation: (2000/2000) * 1920
        '''
        self.assertEqual(width_before, int(2000))
        self.assertEqual(height_before, int(2000))
        self.assertEqual(width_after, int(1920))
        self.assertEqual(height_after, int(1920))
        self.assertEqual(response, {"Changed file!": "Archive was in favorable conditions"})