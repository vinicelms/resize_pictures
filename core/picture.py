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
            self._width_before, self._height_before = self.im.size
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

    def image_size(self):
        return os.stat(full_file_path()).st_size

    def full_file_path(self):
        return "{}{}{}{}".format(self.path, os.path.sep, self.file, self.extension)

    def full_file_path_resized(self):
        if not self._new_directory:
            return "{}{}{}_resized{}".format(self.path, os.path.sep, self.file, self.extension)
        else:
            return "{}{}{}{}{}_resized{}".format(self.path, os.path.sep, self._new_directory, os.path.sep self.file, self.extension)

    def readable_size(self, num):
        for x in ['bytes','KB','MB','GB']:
            if num < 1024.0:
                return "{:3.1f}{}".format(num, x)
            num /= 1024.0
        return "{:3.1f}TB".format(num)

    def resize_picture(self):
        if new_directory:
            os.mkdir("{}{}resized".format(self.path, os.path.sep))

        if self._width_before < 1920 and self._height_before < 1080:
            self._situation = "It will not change"
            self._condition = "Dimensions below standard (Full HD)"
        elif self._width_before == 1920 or self._height_before == 1080:
            self._situation = "It will not change"
            self._condition = "Dimensions are already standardized"
        else:
            d = Dimensions(self._width_before, self._height_before)

            if (self._width_before - 1920) > (self._height_before - 1080):
                self.im = self.im.resize((d.new_width(), 1080))
            else:
                self.im = self.im.resize((1920, d.new_height()))

            self.im.save(full_file_path_resized())

            self._width_after, self._height_before = self.im.size


class Dimension:

    def __init__(self, width, height):
        self._width = width
        self._height = height

    def new_height(self):
        return int((self._height / self._width) * 1920)

    def new_width(self):
        return int((self._width / self._height) * 1080)