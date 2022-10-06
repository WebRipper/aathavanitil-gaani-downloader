import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
from hyper.contrib import HTTP20Adapter
import requests
import string
import time
import os

#####
outdir = "/output/Aathavanitil_Gaani/"
######

songlist = []
list_alpha = []
list_alpha[:0] = string.ascii_lowercase[:26]
for alpha in list_alpha:
  url1 = f"https://www.aathavanitli-gani.com/Anukramanika/{alpha}"
  rqst1 = requests.get(url1)
  for a in rqst1.content.splitlines():
      if ("/Song/" in str(a)) and ("englishName" in str(a)):
          og_url = "https://www.aathavanitli-gani.com"+str(a).split("href")[1].split('"')[1]
          #print(og_url)
          songlist.append(og_url)
  time.sleep(1)
  
files_outdir = os.listdir(outdir)
for song in songlist[1:]:
  og_url = song
  songname = og_url.split("/")[-1]

  if f'{songname}.mp3' in files_outdir:
    print("song skipped")
    continue

  time.sleep(1)
  rqst = requests.get(og_url)
  for a in rqst.content.splitlines():
      if "getSongStream" in str(a):
          ss = str(a).split("..")[-1].split(">")[0][:-1]
          print(ss)
  path1  = ss
  url = "https://www.aathavanitli-gani.com"+path1
  def getHeaders():
      headers = {
          ":authority": "www.aathavanitli-gani.com",
          ":method": "GET",
          ":path": path1,
          ":scheme": "https",
          "referer": og_url
          }
      return headers
  sessions=requests.session()
  sessions.mount('https://www.aathavanitli-gani.com', HTTP20Adapter())
  #r=sessions.post(url,data=playload,headers=getHeaders())
  r=sessions.post(url,headers=getHeaders())
  print(r)

  if str(r) != "<Response [200]>":
    print(og_url)

  if str(r) == "<Response [200]>":
    with open(outdir+f'{songname}.mp3', 'wb') as f:
        f.write(r.content)
