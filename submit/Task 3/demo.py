

import sys
import thread
import time
import requests
from pyquery import PyQuery as pq



def connectURL( j, i): 
    url = sys.argv[1] #'http://localhost:8080/primecheck'
    r = requests.get(url)
    p = pq(r.text)

    for d in p:
        print ("This is the %d iteration :This is the %d concurrent. %s" % (j + 1, i + 1, pq(d).text()))

if __name__=='__main__':
    t = int(sys.argv[3])
    maxJ = int(sys.argv[4])
    maxI = int(sys.argv[2])
    try:
        j = 0
        while(j < maxJ):
            i = 0
            while (i < maxI):
                thread.start_new_thread( connectURL, (j, i, ) )
                i = i + 1
            j = j + 1
            time.sleep(t)

    except:
        print "Error: unable to start thread"
 
    while 1:
        pass

