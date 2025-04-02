import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict
import html

# Load the Blogger backup XML
input_xml = '../backup/blog-backup.xml'
output_sitemap = 'sitemap.xml'

tree = ET.parse(input_xml)
root = tree.getroot()
ns = {'atom': 'http://www.w3.org/2005/Atom'}

# Normalize Blogger URLs to a comparable format
def normalize_url(url):
    return url.replace('http://', 'https://').replace('www.', '').replace('zorphdark.blogspot.com', 'zorphdark.com')

# Generate URL variants to detect all internal link forms
def generate_url_variants(url):
    path = url.split('.com')[-1]
    variants = [
        f'http://zorphdark.blogspot.com{path}',
        f'https://zorphdark.blogspot.com{path}',
        f'http://www.zorphdark.com{path}',
        f'https://www.zorphdark.com{path}',
        f'https://zorphdark.com{path}'
    ]
    return variants

# Extract valid posts excluding comments
posts = []
for entry in root.findall('atom:entry', ns):
    if entry.find('atom:category', ns) is not None:
        for link in entry.findall('atom:link', ns):
            url = link.attrib.get('href', '')
            if link.attrib.get('rel') == 'alternate' and 'showComment' not in url:
                updated = entry.find('atom:updated', ns).text
                posts.append({'url': url.strip(), 'updated': updated.strip()})
                break

print(f"Total valid posts found: {len(posts)}")

# Count internal references using content, summary or fallback
link_counter = defaultdict(int)
for entry in root.findall('atom:entry', ns):
    content_element = entry.find('atom:content', ns)
    if content_element is None:
        content_element = entry.find('atom:summary', ns)
    content_raw = content_element.text if content_element is not None and content_element.text is not None else ''
    content = html.unescape(content_raw)

    for post in posts:
        variants = generate_url_variants(post['url'])
        if any(variant in content for variant in variants):
            link_counter[post['url']] += 1

max_links = max(link_counter.values()) if link_counter else 1

# Compute priority proportional to the number of internal links
for post in posts:
    links_in = link_counter.get(post['url'], 0)
    priority = 0.9 + (links_in / (1 + max_links)) * 0.1
    post['priority'] = round(priority, 2)

# Generate sitemap XML
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for post in posts:
    lastmod = post['updated'].split('T')[0]
    sitemap += f"""  <url>
    <loc>{post['url']}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{post['priority']}</priority>
  </url>\n"""

sitemap += '</urlset>'

with open(output_sitemap, 'w', encoding='utf-8') as f:
    f.write(sitemap)
print(f"Sitemap generated in {output_sitemap}")