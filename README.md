# Forum Image Scraper
## Downloads images from forum threads
##### Only works with forums which doesn't require a login to view and have an incremental pagination 

## Features
- Downloads all image references in a given forum thread. You can define the forum, the thread and required pages in the property file
- Currently also supports linked FB images in the thread. Downloading FB images links takes more time as we need to perform two calls to get the direct image link. You can opt out from downloading FB image links by setting "downloadFb" to False. 

## How to use

- Download the project as a zip file, unzip and move into the folder
- Locate the "input.properties" file and set proprties. Here are some example property values
    - hostSite = https://www.petforums.co.uk
    - thread = https://www.petforums.co.uk/threads/cute-pet-photo-contest.1952
    - pageAppender = /page-
    - startPage = 1
    - endPage = 20
- Verify "inputs.properties" and save.
- Double click "forum-image-scraper.exe"
- If double clicking doesn't work, open a commpand line prompt and run it by typing "forum-image-scraper.exe". This way you will be able to see if there any issues with your property file. 

## How to develop and package
- "forum-image-scraper.py" contains the entire script. Pyinstaller is used to generate the "exe" file


## What Next
- Support more forum types

## License

MIT License

Copyright (c) [2021] [me2cool]

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
