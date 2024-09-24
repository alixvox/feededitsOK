import os
import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime

def update_feed():
    original_feed_url = "https://www.oudaily.com/search/?c%5b%5d=news,sports,culture&f=rss&ips=1080"
    feed = feedparser.parse(original_feed_url)

    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    rss.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    rss.set("xmlns:media", "http://search.yahoo.com/mrss/")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    rss.set("xmlns:wfw", "http://wellformedweb.org/CommentAPI/")
    rss.set("xmlns:sy", "http://purl.org/rss/1.0/modules/syndication/")
    rss.set("xmlns:slash", "http://purl.org/rss/1.0/modules/slash/")

    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = feed.feed.title
    ET.SubElement(channel, "link").text = feed.feed.link
    ET.SubElement(channel, "description").text = feed.feed.description
    ET.SubElement(channel, "language").text = "en-US"

    # Check if the 'updated' attribute exists
    if hasattr(feed.feed, 'updated'):
        ET.SubElement(channel, "lastBuildDate").text = feed.feed.updated
    else:
        # Use the current date and time as a fallback
        ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    ET.SubElement(channel, "copyright").text = "Copyright"
    ET.SubElement(channel, "atom:link", href=original_feed_url, type="application/rss+xml", rel="self")

    for entry in feed.entries:
        item = ET.SubElement(channel, "item")
        
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        ET.SubElement(item, "description").text = entry.summary.strip()
        ET.SubElement(item, "pubDate").text = entry.published
        ET.SubElement(item, "guid").text = entry.id

        # Extract author information
        dc_creator = ET.SubElement(item, "dc:creator")
        dc_creator.text = entry.get("author", "Unknown")

        # Handle enclosures in the links
        for link in entry.links:
            if link.get('rel') == 'enclosure' and link.get('type', '').startswith('image/'):
                img_url = link['href']
                
                # Add media:thumbnail tag
                media_thumbnail = ET.SubElement(item, "media:thumbnail")
                media_thumbnail.set("url", img_url)
                
                # Add media:content tag
                media_content = ET.SubElement(item, "media:content")
                media_content.set("type", link['type'])
                media_content.set("url", img_url)
                
                # Optionally, add media:title tag
                media_title = ET.SubElement(item, "media:title")
                media_title.text = entry.title

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Write the RSS feed to a file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    tree.write("static/new_oudaily.rss", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    update_feed()
