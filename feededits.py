import feedparser
import xml.etree.ElementTree as ET
import re

# Step 1: Fetch and parse the original RSS feed
original_feed_url = "https://freepressokc.com/feed/"
feed = feedparser.parse(original_feed_url)

# Step 2: Create the root element of the new RSS feed
rss = ET.Element("rss", version="2.0")
rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
rss.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
rss.set("xmlns:media", "http://search.yahoo.com/mrss/")
rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
rss.set("xmlns:wfw", "http://wellformedweb.org/CommentAPI/")
rss.set("xmlns:sy", "http://purl.org/rss/1.0/modules/syndication/")
rss.set("xmlns:slash", "http://purl.org/rss/1.0/modules/slash/")

# Step 3: Create and populate the channel element
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = feed.feed.title
ET.SubElement(channel, "link").text = feed.feed.link
ET.SubElement(channel, "description").text = feed.feed.description
ET.SubElement(channel, "language").text = feed.feed.language
ET.SubElement(channel, "lastBuildDate").text = feed.feed.updated
ET.SubElement(channel, "copyright").text = "Copyright"
ET.SubElement(channel, "atom:link", href="https://www.kgou.org/news-from-kgou-public-radio.rss", type="application/rss+xml", rel="self")

# Step 4: Iterate through each item in the original feed
for entry in feed.entries:
    item = ET.SubElement(channel, "item")
    
    # Transform and add elements
    ET.SubElement(item, "title").text = entry.title
    ET.SubElement(item, "link").text = entry.link
    
    # Remove any unnecessary line breaks and whitespaces in the description
    description_text = re.sub(r'\s+', ' ', entry.description).strip()
    ET.SubElement(item, "description").text = description_text
    
    ET.SubElement(item, "pubDate").text = entry.published
    ET.SubElement(item, "guid").text = entry.id
    
    dc_creator = ET.SubElement(item, "dc:creator")
    dc_creator.text = entry.get("author", "Unknown")

    # Handle embedded media in description, assuming it's an image
    if 'img' in entry.description:
        start_index = entry.description.find('src="') + 5
        end_index = entry.description.find('"', start_index)
        img_url = entry.description[start_index:end_index]
        
        media_thumbnail = ET.SubElement(item, "media:thumbnail")
        media_thumbnail.set("url", img_url)
        
        media_content = ET.SubElement(item, "media:content")
        media_content.set("type", "image/jpeg")
        media_content.set("url", img_url)

# Step 5: Save the XML to a file with indentation and consistent formatting
tree = ET.ElementTree(rss)
ET.indent(tree, space="  ")  # Indentation for readability
tree.write("new_freepressokc.xml", encoding="utf-8", xml_declaration=True)

# Optional: Print the XML for verification
with open("new_freepressokc.xml", "r", encoding="utf-8") as file:
    print(file.read())
