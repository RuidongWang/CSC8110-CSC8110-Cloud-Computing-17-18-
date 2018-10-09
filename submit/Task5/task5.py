import pymongo
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

def GetSubInfo(url, post):
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

    # cpu_usage = re.findall(r"per_cpu_usage\":(.+?),\"user", txt)
    cpu_usage = re.findall(r"\"cpu\":{\"usage\":{\"total\":(.+?),\"per_cpu_usage\":", txt)
    # cpu_usage = GetMiddleStr(txt, 'per_cpu_usage":', ',"user"')
    # while (cpu_usage == ''):
    #     txt = GetWebInfo(url)
    #     cpu_usage = GetMiddleStr(txt, 'per_cpu_usage":', ',"user"')
    # print cpu_usage
    # print "cpu"
    # print cpu_usage
    # for i in xrange(len(cpu_usage)):
    #     print i, cpu_usage[i]
    # "memory":{"usage":
    memory_usage = re.findall(r"\"memory\":{\"usage\":(.+?),\"cache\":", txt)
    # print memory_usage
    print type(memory_usage)

    timestamp = re.findall(r"\"timestamp\":\"(.+?)\",", txt)
    # print "memory"
    # for i in xrange(len(memory_usage)):
    #     print i, memory_usage[i]
    post.insert({"name" : name, "CPU_usage" : cpu_usage[-1], "Memory_usage" : memory_usage[-1], "time" : timestamp[-1]})


def connectURL( j, i):
  connection = pymongo.MongoClient('localhost', 3306)
  tdb = connection.CloudComputing
  post = tdb.task_5
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
          GetSubInfo(newurl, post)

if __name__ == '__main__':
    # t = int(sys.argv[3])
    # maxJ = int(sys.argv[4])
    # maxI = int(sys.argv[2])
    try:
        j = 0
        while (j < 10):
            i = 0
            while (i < 1):
                thread.start_new_thread(connectURL, (j, i,))
                i = i + 1
            j = j + 1
            time.sleep(5)

    except:
        print "Error: unable to start thread"

    while 1:
        pass


