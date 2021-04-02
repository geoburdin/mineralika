
from icrawler.builtin import GoogleImageCrawler
import os, cv2

os.mkdir('minerals_cropped_added/')
for root, dirs, files in os.walk('minerals_raw/'):

    f = os.path.basename(root)  # get class name - Amethyst, Onyx, etc
    if len(files) > 22:
        os.mkdir('minerals_cropped_added/' + f)
        i = 0


        google_crawler = GoogleImageCrawler(storage={'root_dir': ('minerals_cropped_added/' + f)})
        google_crawler.crawl(keyword=(f + ' mineral raw'), max_num=1000)
        for file in files:


            try:
                image = cv2.imread(root + '/' + file)  # read the image (OpenCV)
                image = cv2.resize(image, (299, 299))  # resize the image (images are different size)
                cv2.imwrite('minerals_cropped_added/' + f + '/' + str(i) + '.jpeg', image)

                i=i+1
            except Exception as e:
                print(e)

