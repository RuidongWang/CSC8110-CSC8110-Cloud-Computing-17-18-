import re
import requests
import json
from pyquery import PyQuery as pq
import thread
import time


def GetMiddleStr(content,startStr,endStr):
  startIndex = content.index(startStr)
  if startIndex>=0:
    startIndex += len(startStr)
  endIndex = content.index(endStr)
  return content[startIndex:endIndex]

# def GetAllMiddleStr(content, startStr, endStr)


def GetWebInfo(url):
    r = requests.get(url)
    p = pq(r.text)
    a = str(p)
    return a

def GetSubInfo(url):
    txt = GetWebInfo(url)
    # print txt
    string = GetMiddleStr(txt, '"aliases"', '],')
    while (string == ''):
        txt = GetWebInfo(url)
        string = GetMiddleStr(txt, '"aliases"', '],')
    name = GetMiddleStr(string, '["', '",')
    while (name == ''):
        name = GetMiddleStr(string, '["', '",')
    print name

    cpu_usage = re.findall(r"\"cpu\":{\"usage\":{\"total\":(.+?),\"per_cpu_usage\":", txt)
    print "cpu"
    print cpu_usage[-1]
    memory_usage = re.findall(r"\"memory\":{\"usage\":(.+?),\"cache\":", txt)
    print "memory"
    # for i in xrange(len(memory_usage)):
    #     print i, memory_usage[i]
    print memory_usage[-1]
    test_file = open(name + '.csv', 'a')
    test_file.write(cpu_usage[-1] + "," + memory_usage[-1] + "\n")
    # test_file.close()


def connectURL( j, i):
  url = 'http://localhost:81/api/v1.3/subcontainers'
  a = GetWebInfo(url)
  stringname = GetMiddleStr(a, '"subcontainers":[{"name":"/docker/', '"}],')
  while(stringname == ''):
      a = GetWebInfo(url)
      stringname = GetMiddleStr(a, '"subcontainers":[{"name":"/docker/', '"}],')
  namestring = '[{"name":"/docker/' + stringname + '"}]'
  jsonname = json.loads(namestring)
  for ijson in jsonname:
      for k, v in ijson.iteritems():
          newurl = url + v
          print newurl
          GetSubInfo(newurl)


# data = {'cpu':[], 'memory': []}
# test_file = open('test.csv', 'w')
#
# for i in range(60):
#     test_file.write()



if __name__ == '__main__':

    # t = int(sys.argv[3])
    # maxJ = int(sys.argv[4])
    # maxI = int(sys.argv[2])
    try:
        j = 0
        while (j < 50):
            i = 0
            while (i < 1):
                thread.start_new_thread(connectURL, (j, i,))
                i = i + 1
                # time.sleep(5)
            j = j + 1
            time.sleep(1)

    except:
        print "Error: unable to start thread"

    while 1:
        pass
