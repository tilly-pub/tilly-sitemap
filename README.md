# tilly-sitemap

Generate `robots.txt` and `sitemap.xml` for [tilly](https://github.com/tilly-pub/tilly) sites.

## Example robots.txt

[https://tilly-pub.github.io/robots.txt](https://tilly-pub.github.io/robots.txt)

```txt
User-agent: *
Sitemap: https://tilly-pub.github.io/sitemap.xml
```

## Example sitemap.xml


[https://tilly-pub.github.io/sitemap.xml](https://tilly-pub.github.io/sitemap.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://tilly-pub.github.io/</loc>
    </url>
    <url>
        <loc>https://tilly-pub.github.io/all/</loc>
    </url>
    <url>
        <loc>https://tilly-pub.github.io/plugins</loc>
    </url>
    <url>
        <loc>https://tilly-pub.github.io/plugins/sitemap/</loc>
    </url>
</urlset>
```


## Installation

Install this plugin in the same environment as tilly.

```bash
python -m venv .venv
source .venv/bin/activate
pip install tilly-sitemap
```

## Usage

```bash
tilly sitemap
```

