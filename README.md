# Zorphdark Blog Sitemap Generator

This repository contains utilities to generate a custom XML sitemap for [zorphdark.com](https://www.zorphdark.com), based on Blogger export format.

## Features

- Automatically parses Blogger export files.
- Computes sitemap priorities based on internal link structure.
- Outputs Google Search Console compatible `sitemap.xml`.

## Usage

1. Place the Blogger export file in `backup/blog-backup`.
2. Run the generator:
   ```bash
   python3 sitemap/sitemap-generator.py