from PIL import Image
import os, sys

class Dimensions:

    def __init__(self, width, height):
        self._width = width
        self._height = height

    def new_height(self):
        return int((self._height / self._width) * 1920)

    def new_width(self):
        return int((self._width / self._height) * 1080)

class Picture:
    def __init__(self, file, new_directory=None):
        if os.path.isfile(file):
            self.path, self.file = os.path.split(os.path.abspath(file)) # Separate path from filename
            self.file, self.extension = os.path.splitext(self.file) # Separate file name from extension
            self._size_before = self.image_size(self.full_file_path())
            self._readable_size_before = self.readable_size(self._size_before)
            self._size_after = None
            self._readable_size_after = None
            
            self.im = Image.open(self.full_file_path()) # Open image object to get dimensions of file
            self._width_before, self._height_before = self.im.size
            self._width_after, self._height_after = None, None

            self._new_directory = new_directory

            self._situation, self._condition = None, None
        else:
            self.file = None
            self._situation = "It will not change"
            self._condition = "Not a file"

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

    def image_size(self, file):
        return os.stat(file).st_size

    def full_file_path(self):
        return "{}{}{}{}".format(self.path, os.path.sep, self.file, self.extension)

    def full_file_path_resized(self):
        if not self._new_directory:
            return "{}{}{}_resized{}".format(self.path, os.path.sep, self.file, self.extension)
        else:
            return "{}{}{}{}{}_resized{}".format(self.path, os.path.sep, self._new_directory, os.path.sep, self.file, self.extension)

    def readable_size(self, num):
        for x in ['bytes','KB','MB','GB']:
            if num < 1024.0:
                return "{:3.1f}{}".format(num, x)
            num /= 1024.0
        return "{:3.1f}TB".format(num)

    def resize_picture(self):
        if self.file:
            if self._new_directory and not os.path.isdir("{}{}{}".format(self.path, os.path.sep, self._new_directory)):
                    os.mkdir("{}{}{}".format(self.path, os.path.sep, self._new_directory))

            if self._width_before < 1920 and self._height_before < 1080:
                self._situation = "It will not change"
                self._condition = "Dimensions below standard (Full HD)"
                self._width_after = self._width_before
                self._height_after = self._height_before
                self._size_after = self._size_before
                self._readable_size_after = self._readable_size_before
            elif self._width_before == 1920 or self._height_before == 1080:
                self._situation = "It will not change"
                self._condition = "Dimensions are already standardized"
                self._width_after = self._width_before
                self._height_after = self._height_before
                self._size_after = self._size_before
                self._readable_size_after = self._readable_size_before
            else:
                d = Dimensions(self._width_before, self._height_before)

                if (self._width_before - 1920) > (self._height_before - 1080):
                    self.im = self.im.resize((d.new_width(), 1080))
                else:
                    self.im = self.im.resize((1920, d.new_height()))

                self.im.save(self.full_file_path_resized())

                im_res = Image.open(self.full_file_path_resized())
                self._width_after, self._height_before = im_res.size
                self._size_after = self.image_size(self.full_file_path_resized())
                self._readable_size_after = self.readable_size(self._size_after)
                self._situation = "Changed file!"
                self._condition = "Archive was in favorable conditions"
                im_res.close()
        self.im.close()
        return {self._situation: self._condition}

    def change_report(self):
        if self.file:
            report = "File {}\n".format(self.full_file_path())
            report = "{} - Dimensions (before):\n".format(report)
            report = "{} {}| Width: {}\n".format(report, " "*4, self._width_before)
            report = "{} {}| Height: {}\n".format(report, " "*4, self._height_before)
            report = "{} - Dimensions: (after):\n".format(report)
            report = "{} {}| Width: {}\n".format(report, " "*4, self._width_after)
            report = "{} {}| Height: {}\n".format(report, " "*4, self._height_after)
            report = "{} - Size:\n".format(report)
            report = "{} {}| Before: {}\n".format(report, " "*4, self._readable_size_before)
            report = "{} {}| After: {}\n".format(report, " "*4, self._readable_size_after)
            report = "{} - Status:\n".format(report)
            report = "{} {}| Situation: {}\n".format(report, " "*4, self._situation)
            report = "{} {}| Condition: {}\n".format(report, " "*4, self._condition)
            print(report)