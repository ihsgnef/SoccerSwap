import time
import os
import threading

time_gap = 5 * 60

def main():
    os.chdir('../crawlers/enjoyz/')
    cmd = 'scrapy crawl enjoyz'
    while True:
        os.system(cmd)
        time.sleep(time_gap)


if __name__ == '__main__':
    main()
