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

imgExtentions = ["png","jpeg","jpg","gif"]

config = configparser.RawConfigParser()
config_file = open('input.properties', encoding="utf-8")
config.read_file(config_file)

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
pageAppenderBefore = config.get("UserInput", "pageAppenderBefore")
pageAppenderAfter = config.get("UserInput", "pageAppenderAfter")
page = int(config.get("UserInput", "startPage"))
untilPage = int(config.get("UserInput", "endPage"))
smallImageSize = int(config.get("UserInput", "smallImageSize"))
pageValueMultiply = int(config.get("UserInput", "pageValueMultiply"))

if config.get("UserInput", "shouldDownloadSocialLinks")== 'True':
    shouldDownloadSocialLinks = True
else:
    shouldDownloadSocialLinks = False

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

# Create links for FB/Insta attached images
def createSocialMediaUrl(responseText):
    # Separate regex to find potential Insta photos
    socialLinks = []
    instaTags = re.findall("(instagram.min.html#[a-zA-Z]+)+", responseText);
    for instaTag in instaTags:
        instaUrl = "https://www.instagram.com/p/"+instaTag.split("#")[-1]
        socialLinks.append(instaUrl)
    
    # Separate regex to find potential FB photos
    fbTags = re.findall("\d{6,9}_\d{15,17}_\d{16,19}_[o|n]", responseText);
    for fbTag in fbTags:
        fbUrl = "https://facebook.com/"+fbTag.split("_")[1]
        socialLinks.append(fbUrl)
        
    return socialLinks

# Generate FB direct image link and download the photo  
def downloadFBPhoto(url):
    fbResponse = requests.get(url)
    soup = BeautifulSoup(fbResponse.text, 'html.parser') 
    scriptTag =  soup.find('script', type='application/ld+json')
    if scriptTag:
        data = json.loads(scriptTag.string)
        directFBImageLink = data['image']['contentUrl']
        return requestUrl(directFBImageLink)
    else:
        return fbResponse
        
# Generate Insta direct image link and download the photo      
def downloadInstaPhoto(url):
    instaResponse = requestUrl(url).read()
    soup = BeautifulSoup(instaResponse, 'html.parser')
    metaTag =  soup.find('meta', property="og:image")
    if metaTag:
        directInstaImageLink = metaTag['content']
        return requestUrl(directInstaImageLink)
    else:
        return instaResponse
  
# Modify Urls when Url is not complete. Different forums use different releative path formats. This method needs to be simplified.
def modifyUrl(url):
    if url.startswith("//"):
        return '{}{}'.format("http:", url)
    if url.startswith("/"):
        return '{}{}'.format(hostSite, url)
    elif url.startswith("http"):
        return url;
    elif url.find(".") > url.find("/"):
        return '{}{}'.format(hostSite+"/", url)
    else:
        return '{}{}'.format("http://", url)
              
# We now iterate over pages
while untilPage >= page:
    print ("\n\nPARSING PAGE: "+str(page))

    # We create a separate folder for each page
    pageFolder = threadFolder+"/"+str(page)
    if not os.path.isdir(pageFolder):
        os.mkdir(pageFolder)
    
    # We download the page content and look for image references in the page
    response = requests.get(threadUrl+pageAppenderBefore+str(page*pageValueMultiply)+pageAppenderAfter)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    # We also look for lazy loaded attachments and social media links
    anchorTags = soup.findAll('a', attrs={'href': re.compile("(jpeg|jpg|gif|png|facebook|instagram)")})
 
    # We iterate over image and href references and generate a Url list
    urls = []
    for img in img_tags:
        urls.append(modifyUrl(img['src']))
    for anchor in anchorTags:
        urls.append(modifyUrl(anchor['href']))
    
    # We do special processing for FB, Insta images to extract the proper direct link
    if shouldDownloadSocialLinks:
       socialLinks = createSocialMediaUrl(response.text)
       urls  = urls + socialLinks
        
    # We remove duplicates
    urls = list(set(urls))
    
    print("PAGE PARSED SUCCESSFULLY")
    print("DOWNLOADING IMAGES.....\n")

    # We now iterate over all the unique Urls to download images. 
    for url in urls:

        # we provide a unique file name so that we don't save the file in our future executions of the script
        filename = hashlib.md5(url.encode('utf-8')).hexdigest()+".jpg"
        completeName = pageFolder+"/"+filename
        if os.path.isfile(completeName):
            print ("SKIPPED, ALREADY DOWNLOADED: "+url)
            continue
        
        with open(completeName, 'wb') as f:
            try:
                if shouldDownloadSocialLinks:
                    if "facebook.com" in url:
                        result = downloadFBPhoto(url)
                    elif "instagram.com" in url:
                        result = downloadInstaPhoto(url)
                    else:
                        result = requestUrl(url)
                else:
                    result = requestUrl(url)
                    
                if result.headers['content-type'] and not any(x in result.headers['content-type'] for x in imgExtentions):
                    print ("SKIPPED, PROBABLY NOT A IMAGE: "+url)
                    deleteFile(f)
                    continue
                    
                if result.headers['content-length'] and int(result.headers['content-length']) < smallImageSize:
                    print ("SKIPPED, TOO SMALL: "+url)
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
    
   