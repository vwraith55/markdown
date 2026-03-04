#!/usr/bin/env python3
'''
A simple Markdown to HTML compiler.

Usage:
    $ python3 markdown_compiler.py --input_file=example/README.md
    $ python3 markdown_compiler.py --input_file=example/README.md --add_css
'''

import re
import argparse


def compile_inline(text):
    '''
    Converts inline markdown syntax within a line of text to HTML.
    Handles: images, links, bold, italic, inline code.

    >>> compile_inline('hello world')
    'hello world'

    >>> compile_inline('**bold text**')
    '<strong>bold text</strong>'

    >>> compile_inline('*italic text*')
    '<em>italic text</em>'

    >>> compile_inline('`inline code`')
    '<code>inline code</code>'

    >>> compile_inline('[link text](https://example.com)')
    '<a href="https://example.com">link text</a>'

    >>> compile_inline('![alt text](img/photo.jpg)')
    '<img src="img/photo.jpg" alt="alt text"/>'

    >>> compile_inline('**bold** and *italic*')
    '<strong>bold</strong> and <em>italic</em>'
    '''
    # Images must come before links (same syntax but with leading !)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]*)\)', r'<img src="\2" alt="\1"/>', text)

    # Links
    text = re.sub(r'\[([^\]]*)\]\(([^)]*)\)', r'<a href="\2">\1</a>', text)

    # Bold (must come before italic)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    return text


def compile_lines(lines):
    '''
    Converts a list of markdown lines into a single HTML string.

    >>> compile_lines(['# Hello'])
    '<h1>Hello</h1>'

    >>> compile_lines(['## Hello'])
    '<h2>Hello</h2>'

    >>> compile_lines(['### Hello'])
    '<h3>Hello</h3>'

    >>> compile_lines(['just a paragraph'])
    '<p>just a paragraph</p>'

    >>> compile_lines(['> a blockquote'])
    '<blockquote>a blockquote</blockquote>'

    >>> compile_lines([''])
    ''

    >>> compile_lines(['# Heading', '', 'A paragraph.'])
    '<h1>Heading</h1><p>A paragraph.</p>'

    >>> compile_lines(['```', 'code here', '```'])
    '<pre><code>code here</code></pre>'

    >>> compile_lines(['1. first', '2. second', '3. third'])
    '<ol><li>first</li><li>second</li><li>third</li></ol>'

    >>> compile_lines(['- item one', '- item two'])
    '<ul><li>item one</li><li>item two</li></ul>'
    '''
    html = ''
    i = 0
    in_code_block = False
    code_block_content = []
    ol_items = []
    ul_items = []

    def flush_ol():
        nonlocal html, ol_items
        if ol_items:
            html += '<ol>' + ''.join(f'<li>{item}</li>' for item in ol_items) + '</ol>'
            ol_items = []

    def flush_ul():
        nonlocal html, ul_items
        if ul_items:
            html += '<ul>' + ''.join(f'<li>{item}</li>' for item in ul_items) + '</ul>'
            ul_items = []

    while i < len(lines):
        line = lines[i]

        # --- Code block ---
        if line.strip() == '```':
            if not in_code_block:
                flush_ol()
                flush_ul()
                in_code_block = True
                code_block_content = []
            else:
                in_code_block = False
                inner = '\n'.join(code_block_content)
                html += f'<pre><code>{inner}</code></pre>'
            i += 1
            continue

        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue

        # --- Ordered list ---
        ol_match = re.match(r'^\d+\.\s+(.*)', line)
        if ol_match:
            flush_ul()
            ol_items.append(compile_inline(ol_match.group(1)))
            i += 1
            continue
        else:
            flush_ol()

        # --- Unordered list ---
        ul_match = re.match(r'^[-*]\s+(.*)', line)
        if ul_match:
            ul_items.append(compile_inline(ul_match.group(1)))
            i += 1
            continue
        else:
            flush_ul()

        # --- Blank line ---
        if line.strip() == '':
            i += 1
            continue

        # --- Headings ---
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = compile_inline(heading_match.group(2))
            html += f'<h{level}>{content}</h{level}>'
            i += 1
            continue

        # --- Blockquote ---
        if line.startswith('> '):
            content = compile_inline(line[2:])
            html += f'<blockquote>{content}</blockquote>'
            i += 1
            continue

        # --- Paragraph ---
        content = compile_inline(line)
        html += f'<p>{content}</p>'
        i += 1

    # Flush any remaining list
    flush_ol()
    flush_ul()

    return html


def add_css(html):
    '''
    Wraps the HTML in a full page with CSS styling.

    >>> '<style>' in add_css('<h1>Hello</h1>')
    True

    >>> add_css('<p>test</p>').startswith('<!DOCTYPE html>')
    True
    '''
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
    color: #24292e;
    line-height: 1.6;
  }
  h1, h2, h3, h4, h5, h6 {
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
    margin-top: 24px;
  }
  code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: monospace;
  }
  pre {
    background-color: #f6f8fa;
    padding: 16px;
    border-radius: 6px;
    overflow: auto;
  }
  pre code {
    padding: 0;
    background: none;
  }
  blockquote {
    color: #6a737d;
    border-left: 4px solid #dfe2e5;
    padding: 0 1em;
    margin: 0;
  }
  img {
    max-width: 100%;
  }
  a {
    color: #0366d6;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
</head>
<body>
''' + html + '''
</body>
</html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile Markdown to HTML')
    parser.add_argument('--input_file', required=True, help='Path to the input markdown file')
    parser.add_argument('--add_css', action='store_true', help='Wrap output in a full HTML page with CSS')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    html = compile_lines(lines)

    if args.add_css:
        html = add_css(html)

    output_path = 'README.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Output written to {output_path}')