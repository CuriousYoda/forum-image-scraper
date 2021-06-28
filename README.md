# Forum Image Scraper
## Downloads images from forum threads
##### Only works with forums which doesn't require a login to view and have an incremental pagination 

## Features
- Downloads all image references in a given forum thread. You can define the forum, the thread and required pages in the property file
- Currently also supports linked FB/Insta images in the thread. Downloading FB/Insta images takes bit more time as we need to perform two calls to get the direct image link. You can opt out from downloading FB/Insta image links by setting "shouldDownloadSocialLinks" to False. 

## How to use

- Download the project as a zip file, unzip and move into the folder (it's around 11MB)
- Locate the "input.properties" file and set properties. Here are some example property values
    - hostSite = https://www.petforums.co.uk
    - thread = https://www.petforums.co.uk/threads/cute-pet-photo-contest.1952
    - pageAppenderBefore = /page-
    - startPage = 1
    - endPage = 20
- "pageAppenderBefore" is different from forum to forum. You need to check this by visiting an individual page of the thread via the browser. This is the text between the "thread" url and page number. Few examples are below. 
    - https://www.petforums.co.uk/threads/cute-pet-photo-contest.1952/page-/2 - , pageAppenderBefore =  /page-
    - https://www.ar15.com/forums/general/Cat-meme-thread-because-why-the-hell-not-/5-2083401/&page=14 , pageAppenderBefore = /&page=
- Verify "inputs.properties" and save.
- Double click "forum-image-scraper.exe"
- If double clicking doesn't work, open a command line prompt and run it by typing "forum-image-scraper.exe". This way you will be able to see if there are any issues with your property file. 
- Images will be downloaded to a folder one directory up. Folder structure will be as follows.
    - SiteName
        - ThreadName
            - Page

## How to develop and package
- "forum-image-scraper.py" contains the entire script. Pyinstaller is used to generate the "exe" file


## What Next
- Support more forum types

## License

MIT License

Copyright (c) [2021] [[@CuriousYoda](https://twitter.com/CuriousYoda)]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
