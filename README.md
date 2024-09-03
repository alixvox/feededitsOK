# feededitsOK: RSS Feed Reformatter

## Overview

**feededitsOK** is a public service project designed to reformat and enhance the readability of RSS feeds for news sources in Oklahoma and surrounding areas. This project aims to improve the structure and presentation of various local news RSS feeds, ensuring they are compatible with modern RSS readers and providing a more user-friendly experience.

### How It Works

- **Original Feeds**: The project parses and processes RSS feeds from various news outlets, extracting key elements such as titles, links, descriptions, and media content.
- **Reformatted Feeds**: The extracted content is restructured to follow best practices for RSS feeds, offering a cleaner and more consistent format.
- **Output**: The reformatted feeds are made publicly available and can be accessed via the designated IP address or site, which will be finalized and provided below.

### Supported RSS Feeds

This section lists the original RSS feeds currently being reformatted by the project, along with the link to the reformatted version.

1.  **FreePressOKC**
    - **Original RSS Feed**: https://freepressokc.com/feed/
    - **Reformatted RSS Feed**: Link: [random.ip.address.1039/asdjad:8080](http://random.ip.address.1039/asdjad:8080)

### Making Changes/DIY

*This section is only relevant if you intend to make changes to the code or host the service yourself.*

1.  Clone the repository:
    
    `git clone https://github.com/alixvox/feededitsOK.git`
    
2.  Navigate to the project directory:
    
    `cd feededitsOK`
    
3.  Set up the Python environment and install dependencies (if any):
    
    `pip install -r requirements.txt`
    
4.  Run the script to generate the reformatted RSS feed:
    
    `python feededits.py`
    
5.  Serve the RSS feed on your preferred port (e.g., 8000):
    
    `python3 -m http.server 8000`
    
6.  Access the reformatted feed:
    
    `http://<your-vm-ip>:8000/new_feed.xml`
    

### License

This project is released under the MIT License. See the LICENSE file for more information.