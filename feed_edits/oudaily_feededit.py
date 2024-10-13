import os
import requests
import feedparser
from lxml import etree
from datetime import datetime
import time
import json
from urllib import robotparser

def update_feed():
    original_feed_url = "https://www.oudaily.com/search/?c[]=news,sports,culture&f=rss&ips=1080"
    headers_file = 'feed_headers.json'
    robots_url = 'https://www.oudaily.com/robots.txt'

    # Read stored headers
    stored_headers = {}
    if os.path.exists(headers_file):
        with open(headers_file, 'r') as f:
            stored_headers = json.load(f)

    # Prepare request headers
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; feededitsOK/1.0; +https:newson6.com/bot)'
    }
    if 'Last-Modified' in stored_headers:
        request_headers['If-Modified-Since'] = stored_headers['Last-Modified']
    if 'ETag' in stored_headers:
        request_headers['If-None-Match'] = stored_headers['ETag']

    # Check robots.txt
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:
        print(f"Failed to read robots.txt: {e}")
        return

    can_fetch = rp.can_fetch(request_headers['User-Agent'], original_feed_url)
    if not can_fetch:
        print("Fetching is disallowed by robots.txt")
        return

    # Respect crawl-delay
    crawl_delay = rp.crawl_delay(request_headers['User-Agent'])
    if crawl_delay:
        print(f"Respecting crawl-delay of {crawl_delay} seconds")
        time.sleep(crawl_delay)

    try:
        response = requests.get(original_feed_url, headers=request_headers, timeout=10)
        if response.status_code == 304:
            print("Feed not modified since last fetch.")
            return
        elif response.status_code == 200:
            # Store 'Last-Modified' and 'ETag' headers
            new_stored_headers = {}
            if 'Last-Modified' in response.headers:
                new_stored_headers['Last-Modified'] = response.headers['Last-Modified']
            if 'ETag' in response.headers:
                new_stored_headers['ETag'] = response.headers['ETag']
            with open(headers_file, 'w') as f:
                json.dump(new_stored_headers, f)
            # Process the feed
            feed_content = response.content
            feed = feedparser.parse(feed_content)
        elif response.status_code in [429, 503]:
            print(f"Received {response.status_code} error.")
            retry_after = int(response.headers.get('Retry-After', '0'))
            if retry_after > 0:
                print(f"Server asked to retry after {retry_after} seconds.")
                time.sleep(retry_after)
                # Retry once
                response = requests.get(original_feed_url, headers=request_headers, timeout=10)
                if response.status_code == 200:
                    # Store 'Last-Modified' and 'ETag' headers
                    new_stored_headers = {}
                    if 'Last-Modified' in response.headers:
                        new_stored_headers['Last-Modified'] = response.headers['Last-Modified']
                    if 'ETag' in response.headers:
                        new_stored_headers['ETag'] = response.headers['ETag']
                    with open(headers_file, 'w') as f:
                        json.dump(new_stored_headers, f)
                    # Process the feed
                    feed_content = response.content
                    feed = feedparser.parse(feed_content)
                else:
                    print(f"Failed to fetch the feed after retry. Status code: {response.status_code}")
                    return
            else:
                print(f"No Retry-After header. Exiting.")
                return
        elif response.status_code == 404:
            print(f"Feed not found (404).")
            return
        elif response.status_code >= 500:
            print(f"Server error: Status code {response.status_code}")
            return
        else:
            print(f"Failed to fetch the feed. Status code: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred: {e}")
        return

    # Namespaces mapping
    nsmap = {
        'atom': 'http://www.w3.org/2005/Atom',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'media': 'http://search.yahoo.com/mrss/'
    }

    # Create the root <rss> element with namespaces
    rss = etree.Element('rss', nsmap=nsmap)
    rss.set('version', '2.0')

    # Create the <channel> element
    channel = etree.SubElement(rss, 'channel')

    # Populate channel elements
    channel_title = feed.feed.get('title', 'No Title')
    channel_link = feed.feed.get('link', '')
    channel_description = feed.feed.get('description', '')
    channel_language = feed.feed.get('language', 'en-US')
    if 'updated_parsed' in feed.feed:
        channel_lastBuildDate = datetime(*feed.feed.updated_parsed[:6]).strftime('%a, %d %b %Y %H:%M:%S +0000')
    else:
        channel_lastBuildDate = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Build the channel elements
    etree.SubElement(channel, 'title').text = channel_title
    etree.SubElement(channel, 'link').text = channel_link
    etree.SubElement(channel, 'description').text = channel_description
    etree.SubElement(channel, 'language').text = channel_language
    etree.SubElement(channel, 'lastBuildDate').text = channel_lastBuildDate

    # Add <atom:link> element
    atom_link = etree.SubElement(channel, '{http://www.w3.org/2005/Atom}link')
    atom_link.set('href', original_feed_url)
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')

    # Process each entry in the feed
    for entry in feed.entries:

        item = etree.SubElement(channel, 'item')

        # Title
        etree.SubElement(item, 'title').text = entry.get('title', 'No Title')

        # Link
        etree.SubElement(item, 'link').text = entry.get('link', '')

        # Description
        etree.SubElement(item, 'description').text = entry.get('description', '')

        # Publication Date
        if 'published_parsed' in entry:
            pubDate = datetime(*entry.published_parsed[:6]).strftime('%a, %d %b %Y %H:%M:%S +0000')
        else:
            pubDate = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
        etree.SubElement(item, 'pubDate').text = pubDate

        # GUID
        guid_elem = etree.SubElement(item, 'guid')
        guid_text = entry.get('id', entry.get('link', ''))
        guid_elem.text = guid_text
        # Set isPermaLink attribute if necessary
        if not entry.get('guidislink', True):
            guid_elem.set('isPermaLink', 'false')

        # DC:Creator (Author)
        author_name = 'Unavailable'
        if 'author' in entry and entry.author:
            # Extract author's name from "email (Name)" format
            if '(' in entry.author and ')' in entry.author:
                author_name = entry.author.split('(')[-1].strip(' )')
            else:
                author_name = entry.author
        elif 'dc_creator' in entry and entry.dc_creator:
            author_name = entry.dc_creator
        # Add dc:creator element with CDATA
        etree.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = etree.CDATA(author_name)

        # Categories
        if 'tags' in entry and entry.tags:
            for tag in entry.tags:
                etree.SubElement(item, 'category').text = etree.CDATA(tag.term)
        else:
            # Append "Unavailable" if no categories are found
            etree.SubElement(item, 'category').text = etree.CDATA('Unavailable')

        # Media:Content and Media:Thumbnail (Images)
        image_url = None
        if 'enclosures' in entry and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.type and enclosure.type.startswith('image/'):
                    image_url = enclosure.href
                    break
        if image_url:
            # Add media:content element
            media_content = etree.SubElement(item, '{http://search.yahoo.com/mrss/}content')
            media_content.set('url', image_url)
            media_content.set('type', enclosure.type)
            # Add media:thumbnail element
            media_thumbnail = etree.SubElement(item, '{http://search.yahoo.com/mrss/}thumbnail')
            media_thumbnail.set('url', image_url)
        else:
            # Handle items without images if necessary
            pass

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Write the RSS feed to a file with pretty printing
    tree = etree.ElementTree(rss)
    tree.write("static/new_oudaily.rss", encoding="utf-8", xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    update_feed()
