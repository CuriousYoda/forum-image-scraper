import re
import sys
import os
import json
import urllib
from urllib.request import urlopen
import requests
import hashlib
import zlib
import configparser
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.parse import urlparse
import tldextract

# thread url
threadUrl = ""
# host site
hostSite = ""
# start page number, set this to 1 to start from beginning
page = 1 
# end page number, set this to the lage page of the thread to go until the end
untilPage = 1; 
# Page string appender
pageAppender = "/"
# Indicate whether to download FB images too. This takes bit more time as we have to extract the direct url from the source.
downloadFb = True

config = configparser.RawConfigParser()
config_file = open('input.properties', encoding="utf-8")
config.read_file(config_file)

imgExtentions = ["png","jpeg","jpg","gif"]

# We read the user defined website from the properties file
if config.get("UserInput", "hostSite"):
    hostSite = config.get("UserInput", "hostSite")
    print("HOST SITE: "+hostSite+"\n")
else:
    print("DEFINE HOST URL IN PROPERTY FILE")
    exit

# We read the user defined thread from the properties file
if config.get("UserInput", "thread"):
    threadUrl = config.get("UserInput", "thread")
    simpliedThreadName = unquote(threadUrl.split("/")[-1])
    print("DOWNLOADING THREAD: "+simpliedThreadName+"\n")
else:
    print("DEFINE A THREAD IN PROPERTY FILE")
    exit
    
# We read the other properties
pageAppender = config.get("UserInput", "pageAppender")
page = int(config.get("UserInput", "startPage"))
untilPage = int(config.get("UserInput", "endPage"))
smallImageSize = int(config.get("UserInput", "smallImageSize"))
pageValueMultiply = int(config.get("UserInput", "pageValueMultiply"))

if config.get("UserInput", "downloadFB")== 'True':
    downloadFb = True
else:
    downloadFb = False

# We create a separate folder for each website/host
websiteFolder = "../"+tldextract.extract(hostSite).domain
if not os.path.isdir(websiteFolder):
    os.mkdir(websiteFolder)

# We create a separate folder for each thread
threadFolder = websiteFolder+"/"+simpliedThreadName
if not os.path.isdir(threadFolder):
    os.mkdir(threadFolder)

# Requests a url and returns the response   
def requestUrl(url):
    req = urllib.request.Request(
                                    url, 
                                    data=None, 
                                    headers={
                                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                    }
                )
    return urlopen(req)
    
# delete a file   
def deleteFile(f):
    f.close()
    os.remove(f.name)

# Modify Urls from the raw url list 
def appendUrl(urlList, rawUrl):
    for url in rawUrl.split("//"):
        if(len(url) < 10):
            continue
        if url.startswith("/"):
            url = '{}{}'.format(hostSite, url)
        elif url.find(".") < url.find("/"):
            url = '{}{}'.format("http://", url)
        else:
           url = '{}{}'.format(hostSite+"/", url) 
        urlList.append(url)
        if downloadFb:
            facebookRegex = "\d{6,9}_\d{15,17}_\d{16,19}_[o|n]\.(jpeg|jpg|bmp|png|gif|tiff)"
            fbImageFinder = re.compile(facebookRegex)
            facebookPath = fbImageFinder.search(url)
            if facebookPath:
                urlList.append("https://facebook.com/"+ facebookPath.group(0).split("_")[1])
    return urlList
              
# We now iterate over pages
while untilPage >= page:
    print ("\n\nPARSING PAGE: "+str(page))

    # We create a separate folder for each page
    pageFolder = threadFolder+"/"+str(page)
    if not os.path.isdir(pageFolder):
        os.mkdir(pageFolder)
    
    # We download the page content and look for image references in the page
    response = requests.get(threadUrl+pageAppender+str(page*pageValueMultiply))
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    # We also look for lazy loaded attachments
    anchorTags = soup.find_all("a", class_="js-lbImage")

    # We remove duplicates
    urls = []
    img_tags = list(set(img_tags))
    anchorTags = list(set(anchorTags))
    
    # We iterate over image and href references and generate a Url list
    for img in img_tags:
        urls = appendUrl(urls, img['src'])
    for anchor in anchorTags:
        urls = appendUrl(urls, anchor['href'])    
    print("PAGE PARSED SUCCESSFULLY")
    print("DOWNLOADING IMAGES.....\n")

    # We now iterate over all the Urls to download images. 
    for url in urls:
        
        # we provide a unique file name so that we don't save the file in our future executions of the script
        filename = hashlib.md5(url.encode('utf-8')).hexdigest()+".jpg"
        completeName = pageFolder+"/"+filename
        if os.path.isfile(completeName):
            print ("SKIPPED, ALREADY DOWNLOADED: "+url)
            continue
        
        with open(completeName, 'wb') as f:
            try:
                if "facebook" in url and downloadFb:
                    fbResponse = requests.get(url)
                    soup = BeautifulSoup(fbResponse.text, 'html.parser') 
                    data = json.loads(soup.find('script', type='application/ld+json').string)
                    result = requestUrl(data['image']['contentUrl'])                    
                else:
                    result = requestUrl(url)
                
                if result.headers['content-length'] and int(result.headers['content-length']) < smallImageSize:
                    print ("SKIPPED, TOO SMALL: "+url)
                    deleteFile(f)
                    continue
                if result.headers['content-type'] and not any(x in result.headers['content-type'] for x in imgExtentions):
                    print ("SKIPPED, PROBABLY NOT A IMAGE: "+url)
                    deleteFile(f)
                    continue
                response = result.read()
                f.write(response)
                print("\nSUCCESSFUL: "+url)
                print("SAVED AS "+completeName+"\n")
            except Exception as e:
                print("\nERROR: "+url)
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e,"\n")
                deleteFile(f)
                continue
                
    # on to the next page            
    page = page + 1;
    
   