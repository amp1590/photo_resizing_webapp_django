import concurrent.futures
from PIL import Image
from resizeimage import resizeimage
from os import listdir, getpid
from os.path import isfile, join
import os
import shutil #to zip file

SOURCE_DIR = os.path.join('./media/')
TARGET_DIR = os.path.join('./resize_result/static/result/')
MAX_PROCESSES = 4
MAX_THREADS = 2


class ImageResizer(object):

    def __init__(self):
        self.sizes = [[100, 100], [200, 200], [300, 300], [400, 400], [500, 500], [600, 600], [700, 700], [800, 800], [900, 900], [1000, 1000]]

    def execute(self):
        images = self.get_images()
        self.execute_process(images)

    @staticmethod
    def get_images():
        return [file for file in listdir(SOURCE_DIR) if isfile(join(SOURCE_DIR, file))]

    def execute_process(self, images: list):
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_PROCESSES) as process_executor:
            process_futures = process_executor.map(self.resize_image, [(image) for image in images])

            for processed_images in process_futures:
                print("Resized images: {}".format(", ".join(image for image in processed_images)))

    def resize_image(self, image: str):
        pid = getpid()
        print("Running task from process {}".format(pid))

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as thread_executor:
            resized_images = []
            thread_futures = thread_executor.map(self.resize, [(image, size) for size in self.sizes])

            for resized_image in thread_futures:
                resized_images.append(resized_image)

        return resized_images

    @staticmethod
    def resize(args):
        file, size = args

        with Image.open(SOURCE_DIR + file) as image:
            cover = resizeimage.resize_cover(image, size)
            resized_image = TARGET_DIR + '-'.join(str(s) for s in size) + file
            cover.save(resized_image, image.format)

        return resized_image

#if __name__ == "__main__":
def main():
    dir = './photo_upload/static/'
    for file in os.scandir(dir):
        os.remove(file.path)
        print("removed")

    image_resizer = ImageResizer()
    image_resizer.execute()

    #Checking and deleting if the .zip file already exists
    myfile="./resize_result/static/resized_photos.zip"

    ## If file exists, delete it ##
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:    ## Show an error ##
        print("Error: %s file not found" % myfile)

    #Creating a zip file consisting of the resized images
    shutil.make_archive('./resize_result/static/resized_photos', 'zip', './resize_result/static/result')
    