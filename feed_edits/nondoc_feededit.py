import os
import requests
from lxml import etree
import re

def update_feed():
    # Fetch the original feed with a custom User-Agent header
    original_feed_url = "https://nondoc.com/feed/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(original_feed_url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors
    feed_content = response.content

    # Parse the feed content as XML
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(feed_content, parser=parser)

    # Define namespaces
    ns = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wfw': 'http://wellformedweb.org/CommentAPI/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'atom': 'http://www.w3.org/2005/Atom',
        'sy': 'http://purl.org/rss/1.0/modules/syndication/',
        'slash': 'http://purl.org/rss/1.0/modules/slash/',
        'media': 'http://search.yahoo.com/mrss/'
    }

    # Get the <channel> element
    channel = root.find('channel')
    if channel is None:
        print("No channel element found in the RSS feed.")
        return

    # Get all <item> elements
    items = channel.findall('item')
    print(f"Found {len(items)} items in the feed.")

    for item in items:
        # Extract image URL from <post-thumbnail><url>
        post_thumbnail = item.find('post-thumbnail')
        if post_thumbnail is not None:
            url_element = post_thumbnail.find('url')
            if url_element is not None and url_element.text:
                image_url = url_element.text.strip()
                print(f"Found image URL: {image_url}")
            else:
                image_url = None
                print("No URL found in <post-thumbnail>.")
        else:
            image_url = None
            print("No <post-thumbnail> element found.")

        # Add <media:content> and <media:thumbnail> elements
        if image_url:
            media_content = etree.SubElement(item, '{http://search.yahoo.com/mrss/}content')
            media_content.set('url', image_url)
            media_content.set('type', 'image/jpeg')  # Adjust type if necessary
            print("Added <media:content> element.")

            media_thumbnail = etree.SubElement(item, '{http://search.yahoo.com/mrss/}thumbnail')
            media_thumbnail.set('url', image_url)
            print("Added <media:thumbnail> element.")

        # Remove <post-thumbnail> element
        if post_thumbnail is not None:
            item.remove(post_thumbnail)
            print("Removed <post-thumbnail> element.")

        # Clean up <description> element to remove embedded <img> tags
        description = item.find('description')
        if description is not None and description.text:
            desc_text = description.text
            # Remove <img> tags using regex
            desc_text_clean = re.sub(r'<img[^>]*>', '', desc_text)
            description.text = desc_text_clean
            print("Cleaned up <description> element.")

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Write the modified RSS feed to a file with pretty printing
    tree = etree.ElementTree(root)
    tree.write(
        "static/new_nondoc.rss",
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True
    )
    print("Modified RSS feed has been written to static/new_nondoc.rss.")

if __name__ == "__main__":
    update_feed()
