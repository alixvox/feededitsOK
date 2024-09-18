import os
import feedparser
import xml.etree.ElementTree as ET
import re

def update_feed():
    original_feed_url = "https://www.okenergytoday.com/feed/"
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
    ET.SubElement(channel, "language").text = "en-US"  # Default language setting
    ET.SubElement(channel, "lastBuildDate").text = feed.feed.updated
    ET.SubElement(channel, "copyright").text = "Copyright"
    ET.SubElement(channel, "atom:link", href="https://www.okenergytoday.com/feed/", type="application/rss+xml", rel="self")

    for entry in feed.entries:
        item = ET.SubElement(channel, "item")
        
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link

        # Improved description extraction and cleanup for multiple cases
        description_html = entry.description

        # Remove unwanted parts like "Continue reading" and any extra "The post..." text
        description_cleaned = re.sub(r'<p.*?>', '', description_html)  # Remove opening <p> tags
        description_cleaned = re.sub(r'</p>', ' ', description_cleaned)  # Replace closing </p> with space
        description_cleaned = re.sub(r'(<a.*?>.*?</a>|Continue reading.*|The post .* first appeared on .*)', '', description_cleaned)  # Remove links, "Continue reading", and "The post..." text

        # Remove excessive whitespace and HTML entities (like &#160;)
        description_cleaned = re.sub(r'&#\d+;', ' ', description_cleaned)  # Replace HTML entities with spaces
        description_cleaned = re.sub(r'\s+', ' ', description_cleaned).strip()  # Remove excess whitespace

        # Shorten the description if needed, and add ellipsis if too long
        if len(description_cleaned) > 300:  # Optional: Limit description to 300 characters
            description_cleaned = description_cleaned[:300].rsplit(' ', 1)[0] + '...'

        # Set the cleaned description
        ET.SubElement(item, "description").text = description_cleaned

        ET.SubElement(item, "pubDate").text = entry.published
        ET.SubElement(item, "guid").text = entry.id

        dc_creator = ET.SubElement(item, "dc:creator")
        dc_creator.text = entry.get("author", "Unknown")

        # Handle embedded media, extracting the image and related details
        if 'img' in description_html:
            # Extract the URL for the image
            img_start_index = description_html.find('src="') + 5
            img_end_index = description_html.find('"', img_start_index)
            img_url = description_html[img_start_index:img_end_index]

            # Add media:thumbnail and media:content
            media_thumbnail = ET.SubElement(item, "media:thumbnail")
            media_thumbnail.set("url", img_url)

            media_content = ET.SubElement(item, "media:content")
            media_content.set("type", "image/jpeg")
            media_content.set("url", img_url)

            # Extract and map alt text to media:title if available
            alt_start = description_html.find('alt="') + 5
            alt_end = description_html.find('"', alt_start)
            if alt_start > 4 and alt_end > alt_start:
                alt_text = description_html[alt_start:alt_end]
                media_title = ET.SubElement(item, "media:title")
                media_title.text = alt_text

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Write the updated RSS feed to an XML file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    tree.write("static/new_okenergytoday.rss", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    update_feed()
