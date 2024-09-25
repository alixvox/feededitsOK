import os
import feedparser
import re
from lxml import etree
from datetime import datetime

def update_feed():
    # Parse the original feed
    original_feed_url = "https://freepressokc.com/feed/"
    feed = feedparser.parse(original_feed_url)

    nsmap = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wfw': 'http://wellformedweb.org/CommentAPI/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'atom': 'http://www.w3.org/2005/Atom',
        'sy': 'http://purl.org/rss/1.0/modules/syndication/',
        'slash': 'http://purl.org/rss/1.0/modules/slash/',
        'media': 'http://search.yahoo.com/mrss/'
    }
    
    # Create the root <rss> element with namespaces
    rss = etree.Element('rss', nsmap=nsmap)
    rss.set('version', '2.0')
    channel = etree.SubElement(rss, "channel")

    # Add channel elements
    etree.SubElement(channel, "title").text = feed['feed'].get('title', '')
    etree.SubElement(channel, "link").text = feed['feed'].get('link', '')
    etree.SubElement(channel, "description").text = feed['feed'].get('description', '')

    # lastBuildDate
    if 'updated_parsed' in feed['feed']:
        lastBuildDate = datetime(*feed['feed']['updated_parsed'][:6]).strftime('%a, %d %b %Y %H:%M:%S +0000')
    else:
        lastBuildDate = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    etree.SubElement(channel, "lastBuildDate").text = lastBuildDate

    etree.SubElement(channel, "language").text = feed['feed'].get('language', 'en-US')

    # sy:updatePeriod
    sy_updatePeriod = etree.SubElement(channel, "{http://purl.org/rss/1.0/modules/syndication/}updatePeriod")
    sy_updatePeriod.text = "hourly"

    # sy:updateFrequency
    sy_updateFrequency = etree.SubElement(channel, "{http://purl.org/rss/1.0/modules/syndication/}updateFrequency")
    sy_updateFrequency.text = "1"

    # generator
    etree.SubElement(channel, "generator").text = feed['feed'].get('generator', 'Custom Script')

    # atom:link
    atom_link = etree.SubElement(channel, "{http://www.w3.org/2005/Atom}link", rel="self", type="application/rss+xml", href=original_feed_url)

    # image
    if 'image' in feed['feed']:
        image = etree.SubElement(channel, "image")
        etree.SubElement(image, "url").text = feed['feed']['image'].get('href', '')
        etree.SubElement(image, "title").text = feed['feed']['image'].get('title', '')
        etree.SubElement(image, "link").text = feed['feed']['image'].get('link', '')
        # Optionally add width and height if available
        if 'width' in feed['feed']['image']:
            etree.SubElement(image, "width").text = str(feed['feed']['image']['width'])
        if 'height' in feed['feed']['image']:
            etree.SubElement(image, "height").text = str(feed['feed']['image']['height'])

    # Process items
    for entry in feed['entries']:
        item = etree.SubElement(channel, "item")

        # title
        etree.SubElement(item, "title").text = entry.get('title', '')

        # link
        etree.SubElement(item, "link").text = entry.get('link', '')

        # dc:creator
        dc_creator = etree.SubElement(item, "{http://purl.org/dc/elements/1.1/}creator")
        dc_creator.text = entry.get('author', '')

        # pubDate
        if 'published_parsed' in entry:
            pubDate = datetime(*entry.published_parsed[:6]).strftime('%a, %d %b %Y %H:%M:%S +0000')
        elif 'updated_parsed' in entry:
            pubDate = datetime(*entry.updated_parsed[:6]).strftime('%a, %d %b %Y %H:%M:%S +0000')
        else:
            pubDate = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
        etree.SubElement(item, "pubDate").text = pubDate

        # guid
        guid = etree.SubElement(item, "guid", isPermaLink="false")
        guid.text = entry.get('id', entry.get('link', ''))

        # categories
        if 'tags' in entry:
            for tag in entry['tags']:
                category = etree.SubElement(item, "category")
                category.text = tag.get('term', '')

        # description (simplified)
        description = entry.get('description', '') or entry.get('summary', '')
        # Remove <img> tags from description
        description_cleaned = re.sub(r'<img.*?>', '', description, flags=re.DOTALL)
        description_cleaned = description_cleaned.strip()
        etree.SubElement(item, "description").text = etree.CDATA(description_cleaned)

        # Extract image URL from original description
        img_match = re.search(r'<img[^>]+src="([^"]+)"', entry.get('description', ''), flags=re.DOTALL)
        if img_match:
            image_url = img_match.group(1)
            # Add media:thumbnail and media:content
            etree.SubElement(item, "{http://search.yahoo.com/mrss/}thumbnail", url=image_url)
            etree.SubElement(item, "{http://search.yahoo.com/mrss/}content", url=image_url, type="image/jpeg")
        else:
            # Handle case where no image is found
            pass

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)
    
    # Write the RSS feed to a file with pretty printing
    tree = etree.ElementTree(rss)
    tree.write("static/new_freepressokc.rss", encoding="utf-8", xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    update_feed()
