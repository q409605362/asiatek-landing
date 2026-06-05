#!/usr/bin/env python3
import re

with open('/tmp/asiatek-landing/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix duplicate data-i18n attributes
# Pattern: data-i18n="X" data-i18n="Y"
content = re.sub(r'data-i18n="([^"]+)"\s+data-i18n="([^"]+)"', r'data-i18n="\1"', content)

# Fix closing tags that have />
content = re.sub(r'</([^/]+)//', r'</\1>', content)

with open('/tmp/asiatek-landing/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Duplicates fixed!")
