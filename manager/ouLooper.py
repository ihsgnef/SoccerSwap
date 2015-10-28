import time
import os
import threading

time_gap = 3 * 60

def main():
    os.chdir('../crawlers/ouou/')
    cmd = 'scrapy crawl ouou'
    while True:
        os.system(cmd)
        time.sleep(time_gap)


if __name__ == '__main__':
    main()
