from PIL import Image
import os, sys

class Picture:
    def __init__(self, file, new_directory=None):
        if os.path.isfile(file):
            self.path, self.file = os.path.split(os.path.abspath(file)) # Separate path from filename
            self.file, self.extension = os.path.splitext(self.file) # Separate file name from extension
            self._size_before = image_size()
            self._readable_size_before = readable_size(self.size_before)
            self._size_after = None
            self._readable_size_after = None
            
            self.im = Image.open(full_file_path()) # Open image object to get dimensions of file
            self._width_before, self._height_before = im.size
            self._width_after, self._height_after = None, None

            self._new_directory = new_directory

            self._situation, self._condition = None, None
        else:
            raise TypeError

    @property
    def size_before(self):
        return self._size_before

    @property
    def size_after(self):
        return self._size_after

    @property
    def readable_size_before(self):
        return self._readable_size_before

    @property
    def readable_size_after(self):
        return self._readable_size_after

    @property
    def width_before(self):
        return self._width_before

    @property
    def width_after(self):
        return self._width_after

    @property
    def height_before(self):
        return self._height_before

    @property
    def height_after(self):
        return self._height_after