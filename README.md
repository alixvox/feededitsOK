# feededitsOK: RSS Feed Reformatter

## Overview

**feededitsOK** is a public service project designed to reformat and enhance the readability of RSS feeds for news sources in Oklahoma and surrounding areas! This started as a passion project for me when incorporating my personal custom daily RSS reader with other Oklahoman news sources, and I quickly gained the knowledge that there are many ways of populating an RSS feed, most of which need dedicated interpreters that account for every possible attribute the XML format may include. This project aims to improve the structure and presentation of various local news RSS feeds, ensuring they are compatible with modern RSS readers and providing a more user-friendly experience.

### How It Works

- **Original Feeds**: The project parses and processes RSS feeds from various news outlets, extracting key elements such as titles, links, descriptions, and media content.
- **Reformatted Feeds**: The extracted content is restructured to follow best practices for RSS feeds, offering a cleaner and more consistent format.
- **Output**: The reformatted feeds can be hosted anywhere, locally or internally that is, as they are public news feeds not intended for repurposing.

### Supported RSS Feeds

1. **FreePressOKC**
   - **Original RSS Feed**: https://freepressokc.com/feed/
2. **Nondoc Media**
   * **Original RSS Feed:** https://nondoc.com/feed/
3. **OK Sun & Energy**
   * **Original RSS Feed:** https://www.okenergytoday.com/feed/
4. **OU Daily**
   1. **Original RSS Feed:** https://www.oudaily.com/search/?c[]=news,sports,culture&f=rss&ips=1080

### Making Changes/DIY

*This section is only relevant if you intend to make changes to the code or host the service yourself.*

1. Clone the repository:

   `git clone https://github.com/alixvox/feededitsOK.git`
2. Navigate to the project directory:

   `cd feededitsOK`
3. Set up the Python environment and install dependencies (if any):

   `pip install -r requirements.txt`
4. Run the script to generate the reformatted RSS feed:

   `python feededits.py`
5. Serve the RSS feed on your preferred port (e.g., 8000):

   `python3 -m http.server 8000`
6. Access the reformatted feed:

   `http://<your-vm-ip>:8000/new_feed.xml`

### License

This project is released under the MIT License. See the LICENSE file for more information.
