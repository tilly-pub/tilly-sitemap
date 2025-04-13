import os
import re
import pathlib

import click
from click import echo
from click_default_group import DefaultGroup

from tilly.plugin import hookimpl
from tilly.utils import add_config_to_env, static_folder

from datasette.app import Datasette
from asgiref.sync import async_to_sync


root = pathlib.Path.cwd()

@hookimpl
def til_command(cli):
    @cli.group(
        cls=DefaultGroup,
        default="default",
        default_if_no_args=True,
    )
    @click.version_option(message="tilly-sitemap, version %(version)s")
    def sitemap():
        """Generate sitemap.xml for tilly sites."""

    @sitemap.command("default")
    def default():
        add_config_to_env()
        sitemap = sitemap_xml()
        write_sitemap(sitemap)
        update_robot_sitemap_url()


@async_to_sync
async def sitemap_xml():
    ds = Datasette(files=["tils.db"])

    base_url = os.environ.get('TILLY_BASE_URL')

    content = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" ',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml" ',
        '        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    ]

    paths = ["", "all"]

    # Add any configured using the SQL query
    db = ds.get_database()

    # Sitemap limit is 50,000
    limit = 50000 - len(paths)
    for row in await db.execute(f"""
        SELECT DISTINCT SUBSTR(topics, 1, INSTR(topics || ',', ',') - 1) as path FROM til
        UNION
        SELECT url as path FROM til
        LIMIT {limit}
    """
    ):
        try:
            path = row["path"]
        except IndexError:
            raise ValueError("SQL query must return a path column")
        paths.append(row["path"])

    # Verify those paths
    for path in paths:
        path = path.replace('.md', '/')
        path = f"{base_url}/{path}"
        path = add_trailing_slash(path)
        content.append("<url>")
        content.append(f"<loc>{path}</loc>")
        content.append("</url>\n")
    content.append("</urlset>")
    return content

def add_trailing_slash(input_string):
    print(input_string)
    if not input_string.endswith('/'):
        return input_string + '/'
    return input_string

def write_sitemap(sitemap):
    path = root / static_folder() / "sitemap.xml"
    echo(f"write_sitemap to {path}")

    sitemap_xml = "\n".join(sitemap)
    path.write_text(sitemap_xml)



def update_robot_sitemap_url():
    """
    Update the sitemap URL in the robots.txt file.

    :return: Boolean indicating if the update was successful
    """
    robots_file_path = root / static_folder() / "robots.txt"
    robots_file_path.touch()

    base_url = os.environ.get('TILLY_BASE_URL')
    if base_url is None:
        raise KeyError("Add the base url of your site to the config (tilly config -l --base-url https://<>)")

    sitemap_url = f"{base_url}/sitemap.xml"

    try:
        # Read the contents of the robots.txt file
        with open(robots_file_path, 'r') as file:
            lines = file.readlines()

        # Find and replace the sitemap line
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().lower().startswith('sitemap:'):
                new_lines.append(f'Sitemap: {sitemap_url}\n')
                updated = True
            else:
                new_lines.append(line)

        # If no sitemap directive was found, append one
        if not updated:
            new_lines.append(f'Sitemap: {sitemap_url}\n')
            updated = True

        # Write the updated content back to the file
        with open(robots_file_path, 'w') as file:
            file.writelines(new_lines)

        return updated

    except IOError as e:
        print(f"An error occurred while accessing the file: {e}")
        return False


