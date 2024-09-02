import feedparser
import xml.etree.ElementTree as ET
import re

def update_feed():
    original_feed_url = "https://freepressokc.com/feed/"
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
    ET.SubElement(channel, "language").text = feed.feed.language
    ET.SubElement(channel, "lastBuildDate").text = feed.feed.updated
    ET.SubElement(channel, "copyright").text = "Copyright"
    ET.SubElement(channel, "atom:link", href="https://www.kgou.org/news-from-kgou-public-radio.rss", type="application/rss+xml", rel="self")

    for entry in feed.entries:
        item = ET.SubElement(channel, "item")
        
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        
        # Extract the paragraph after the main hyperlink and before "Get more Oklahoma City news"
        description_html = entry.description
        paragraph_match = re.search(r'</a><p>(.*?)</p>', description_html)
        if paragraph_match:
            description_text = paragraph_match.group(1)
        else:
            description_text = "Description not found."

        ET.SubElement(item, "description").text = description_text.strip()
        
        ET.SubElement(item, "pubDate").text = entry.published
        ET.SubElement(item, "guid").text = entry.id
        
        dc_creator = ET.SubElement(item, "dc:creator")
        dc_creator.text = entry.get("author", "Unknown")

        # Handle embedded media, mapping alt text and src
        if 'img' in description_html:
            start_index = description_html.find('src="') + 5
            end_index = description_html.find('"', start_index)
            img_url = description_html[start_index:end_index]
            
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

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    tree.write("static/new_freepressokc.rss", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    update_feed()
