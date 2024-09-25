import os
import feedparser
from lxml import etree
from datetime import datetime
import re
import html

def update_feed():
    # Parse the original feed
    original_feed_url = "https://www.okenergytoday.com/feed/"
    feed = feedparser.parse(original_feed_url)

    # Namespaces
    nsmap = {
        # Removed the default namespace mapping
        # None: 'http://www.w3.org/2005/Atom',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wfw': 'http://wellformedweb.org/CommentAPI/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'atom': 'http://www.w3.org/2005/Atom',
        'sy': 'http://purl.org/rss/1.0/modules/syndication/',
        'slash': 'http://purl.org/rss/1.0/modules/slash/',
        'georss': 'http://www.georss.org/georss',
        'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
        'media': 'http://search.yahoo.com/mrss/'
    }

    # Create root RSS element
    rss = etree.Element('rss', version='2.0', nsmap=nsmap)

    # Create channel element
    channel = etree.SubElement(rss, 'channel')

    # Add channel information
    etree.SubElement(channel, 'title').text = feed.feed.get('title', 'OK Energy Today')
    etree.SubElement(channel, 'link').text = feed.feed.get('link', 'https://www.okenergytoday.com')
    etree.SubElement(channel, 'description').text = feed.feed.get('description', 'Energy News Just A Click Away')
    etree.SubElement(channel, 'lastBuildDate').text = feed.feed.get('updated', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000'))
    etree.SubElement(channel, 'language').text = feed.feed.get('language', 'en-US')

    # Add atom:link element
    atom_link = etree.SubElement(channel, etree.QName(nsmap['atom'], 'link'))
    atom_link.set('href', feed.feed.get('href', original_feed_url))
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')

    # Add generator
    etree.SubElement(channel, 'generator').text = 'Custom Python Script'

    # Process each entry
    for entry in feed.entries:
        item = etree.SubElement(channel, 'item')

        # Title
        etree.SubElement(item, 'title').text = entry.get('title', 'No Title')

        # Link
        etree.SubElement(item, 'link').text = entry.get('link', '')

        # GUID
        guid = etree.SubElement(item, 'guid', isPermaLink='false')
        guid.text = entry.get('id', '')

        # Publication Date
        pub_date = entry.get('published', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000'))
        etree.SubElement(item, 'pubDate').text = pub_date

        # Description
        description = entry.get('summary', '')
        etree.SubElement(item, 'description').text = etree.CDATA(description)

        # DC:Creator
        dc_creator = etree.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator')
        dc_creator.text = entry.get('author', 'Unknown')

        # Categories
        categories = entry.get('tags', [])
        if categories:
            for tag in categories:
                category = etree.SubElement(item, 'category')
                category.text = tag.get('term', 'Unavailable')
        else:
            # Add 'Unavailable' category if no categories are found
            category = etree.SubElement(item, 'category')
            category.text = 'Unavailable'

        # Extract image from content or description
        image_url = None

        # Try content:encoded
        content_encoded = entry.get('content', [])
        if content_encoded:
            content_html = content_encoded[0].value
        else:
            content_html = entry.get('summary', '')

        # Unescape HTML entities
        content_html = html.unescape(content_html)

        # Use regex to find the first img tag
        img_match = re.search(r'<img[^>]+src="([^">]+)"', content_html)
        if img_match:
            image_url = img_match.group(1)

        if not image_url:
            # Use placeholder image if no image is found
            # Placeholder image URL (solid color image)
            placeholder_image_url = 'https://griffin-communications.akamaized.net/WebPages/news-aggregation/2024/oket-placeholder.jpg'
            image_url = placeholder_image_url

        # Add media:content and media:thumbnail
        media_content = etree.SubElement(item, '{http://search.yahoo.com/mrss/}content', url=image_url, type='image/jpeg')
        media_thumbnail = etree.SubElement(item, '{http://search.yahoo.com/mrss/}thumbnail', url=image_url)

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Write the RSS feed to a file with pretty printing
    tree = etree.ElementTree(rss)
    tree.write("static/new_okenergytoday.rss", encoding="utf-8", xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    update_feed()
