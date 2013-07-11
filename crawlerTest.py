#!/usr/bin/python
# -*- coding: utf-8 -*-

import CnkiCrawler
import sys
import codecs
try:
    type = sys.getfilesystemencoding()
    reload(sys) 
    sys.setdefaultencoding('utf-8')
    cnkiCrawler=CnkiCrawler.CnkiCrawler([],ExtraOutInfo=False)
    cnkiCrawler.setOutputHandler(CnkiCrawler.printSplitData2Screen)
   # cnkiCrawler.crawl('google'.encode('utf-8'),mode=1)
    cnkiCrawler.crawl(sys.argv[1].decode(type).encode('utf-8'),mode=1)
except:
    print sys.exc_info()
