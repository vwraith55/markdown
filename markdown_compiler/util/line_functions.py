'''
Each of the functions in this file takes a single line of input
and transforms the line in some way.
'''


def compile_headers(line):
    '''
    Convert markdown headers into <h1>,<h2>,etc tags.

    >>> compile_headers('# This is the main header')
    '<h1> This is the main header</h1>'
    >>> compile_headers('## This is a sub-header')
    '<h2> This is a sub-header</h2>'
    >>> compile_headers('### This is a sub-header')
    '<h3> This is a sub-header</h3>'
    >>> compile_headers('#### This is a sub-header')
    '<h4> This is a sub-header</h4>'
    >>> compile_headers('##### This is a sub-header')
    '<h5> This is a sub-header</h5>'
    >>> compile_headers('###### This is a sub-header')
    '<h6> This is a sub-header</h6>'
    >>> compile_headers('      # this is not a header')
    '      # this is not a header'
    '''
    for level in range(6, 0, -1):
        prefix = '#' * level
        if line[:level] == prefix and (
            len(line) == level or line[level] != '#'
        ):
            rest = line[level:]
            return f'<h{level}>{rest}</h{level}>'
    return line


def compile_italic_star(line):
    '''
    Convert "*italic*" into "<i>italic</i>".

    >>> compile_italic_star('*This is italic!* This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_star('*This is italic!*')
    '<i>This is italic!</i>'
    >>> compile_italic_star('This is *italic*!')
    'This is <i>italic</i>!'
    >>> compile_italic_star('This is not *italic!')
    'This is not *italic!'
    >>> compile_italic_star('*')
    '*'
    '''
    start = line.find('*')
    if start == -1:
        return line
    end = line.find('*', start + 1)
    if end == -1:
        return line
    return line[:start] + '<i>' + line[start + 1:end] + '</i>' + line[end + 1:]


def compile_italic_underscore(line):
    '''
    Convert "_italic_" into "<i>italic</i>".

    >>> compile_italic_underscore('_This is italic!_ This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_underscore('_This is italic!_')
    '<i>This is italic!</i>'
    >>> compile_italic_underscore('This is _italic_!')
    'This is <i>italic</i>!'
    >>> compile_italic_underscore('This is not _italic!')
    'This is not _italic!'
    >>> compile_italic_underscore('_')
    '_'
    '''
    start = line.find('_')
    if start == -1:
        return line
    end = line.find('_', start + 1)
    if end == -1:
        return line
    return line[:start] + '<i>' + line[start + 1:end] + '</i>' + line[end + 1:]


def compile_strikethrough(line):
    '''
    Convert "~~strikethrough~~" to "<ins>strikethrough</ins>".

    >>> compile_strikethrough('~~This is strikethrough!~~ This is not strikethrough.')
    '<ins>This is strikethrough!</ins> This is not strikethrough.'
    >>> compile_strikethrough('~~This is strikethrough!~~')
    '<ins>This is strikethrough!</ins>'
    >>> compile_strikethrough('This is ~~strikethrough~~!')
    'This is <ins>strikethrough</ins>!'
    >>> compile_strikethrough('This is not ~~strikethrough!')
    'This is not ~~strikethrough!'
    >>> compile_strikethrough('~~')
    '~~'
    '''
    start = line.find('~~')
    if start == -1:
        return line
    end = line.find('~~', start + 2)
    if end == -1:
        return line
    return (
        line[:start]
        + '<ins>'
        + line[start + 2:end]
        + '</ins>'
        + line[end + 2:]
    )


def compile_bold_stars(line):
    '''
    Convert "**bold**" to "<b>bold</b>".

    >>> compile_bold_stars('**This is bold!** This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_stars('**This is bold!**')
    '<b>This is bold!</b>'
    >>> compile_bold_stars('This is **bold**!')
    'This is <b>bold</b>!'
    >>> compile_bold_stars('This is not **bold!')
    'This is not **bold!'
    >>> compile_bold_stars('**')
    '**'
    '''
    start = line.find('**')
    if start == -1:
        return line
    end = line.find('**', start + 2)
    if end == -1:
        return line
    return (
        line[:start]
        + '<b>'
        + line[start + 2:end]
        + '</b>'
        + line[end + 2:]
    )


def compile_bold_underscore(line):
    '''
    Convert "__bold__" to "<b>bold</b>".

    >>> compile_bold_underscore('__This is bold!__ This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_underscore('__This is bold!__')
    '<b>This is bold!</b>'
    >>> compile_bold_underscore('This is __bold__!')
    'This is <b>bold</b>!'
    >>> compile_bold_underscore('This is not __bold!')
    'This is not __bold!'
    >>> compile_bold_underscore('__')
    '__'
    '''
    start = line.find('__')
    if start == -1:
        return line
    end = line.find('__', start + 2)
    if end == -1:
        return line
    return (
        line[:start]
        + '<b>'
        + line[start + 2:end]
        + '</b>'
        + line[end + 2:]
    )


def compile_code_inline(line):
    '''
    Add <code> tags.

    >>> compile_code_inline('You can use backticks like this (`1+2`) to include code in the middle of text.')
    'You can use backticks like this (<code>1+2</code>) to include code in the middle of text.'
    >>> compile_code_inline('This is inline code: `1+2`')
    'This is inline code: <code>1+2</code>'
    >>> compile_code_inline('`1+2`')
    '<code>1+2</code>'
    >>> compile_code_inline('This example has html within the code: `<b>bold!</b>`')
    'This example has html within the code: <code>&lt;b&gt;bold!&lt;/b&gt;</code>'
    >>> compile_code_inline('this example has a math formula in the  code: `1 + 2 < 4`')
    'this example has a math formula in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('this example has a <b>math formula</b> in the  code: `1 + 2 < 4`')
    'this example has a <b>math formula</b> in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('```')
    '```'
    >>> compile_code_inline('```python3')
    '```python3'
    '''
    start = line.find('`')
    if start == -1:
        return line
    # skip triple backticks (code blocks)
    if line[start:start+ 3] == '```':
        return line
    end = line.find('`', start + 1)
    if end == -1:
        return line
    inner = line[start + 1:end]
    inner = inner.replace('<', '&lt;').replace('>', '&gt;')
    return line[:start] + '<code>' + inner + '</code>' + line[end + 1:]


def compile_links(line):
    '''
    Add <a> tags.

    >>> compile_links('Click on the [course webpage](https://github.com/mikeizbicki/cmc-csci040)!')
    'Click on the <a href="https://github.com/mikeizbicki/cmc-csci040">course webpage</a>!'
    >>> compile_links('[course webpage](https://github.com/mikeizbicki/cmc-csci040)')
    '<a href="https://github.com/mikeizbicki/cmc-csci040">course webpage</a>'
    >>> compile_links('this is wrong: [course webpage]    (https://github.com/mikeizbicki/cmc-csci040)')
    'this is wrong: [course webpage]    (https://github.com/mikeizbicki/cmc-csci040)'
    >>> compile_links('this is wrong: [course webpage](https://github.com/mikeizbicki/cmc-csci040')
    'this is wrong: [course webpage](https://github.com/mikeizbicki/cmc-csci040'
    '''
    # must not be an image (no leading !)
    bracket_open = line.find('[')
    if bracket_open == -1:
        return line
    # images have ! before [
    if bracket_open > 0 and line[bracket_open - 1] == '!':
        return line
    bracket_close = line.find(']', bracket_open)
    if bracket_close == -1:
        return line
    # paren must immediately follow ]
    if bracket_close + 1 >= len(line) or line[bracket_close + 1] != '(':
        return line
    paren_open = bracket_close + 1
    paren_close = line.find(')', paren_open)
    if paren_close == -1:
        return line
    text = line[bracket_open + 1:bracket_close]
    url = line[paren_open + 1:paren_close]
    return (
        line[:bracket_open]
        + f'<a href="{url}">{text}</a>'
        + line[paren_close + 1:]
    )


def compile_images(line):
    '''
    Add <img> tags.

    >>> compile_images('[Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    '[Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)'
    >>> compile_images('![Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    '<img src="https://avatars1.githubusercontent.com/u/1052630?v=2&s=460" alt="Mike Izbicki" />'
    >>> compile_images('This is an image of Mike Izbicki: ![Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    'This is an image of Mike Izbicki: <img src="https://avatars1.githubusercontent.com/u/1052630?v=2&s=460" alt="Mike Izbicki" />'
    '''
    exclaim = line.find('![')
    if exclaim == -1:
        return line
    bracket_open = exclaim + 1
    bracket_close = line.find(']', bracket_open)
    if bracket_close == -1:
        return line
    if bracket_close + 1 >= len(line) or line[bracket_close + 1] != '(':
        return line
    paren_open = bracket_close + 1
    paren_close = line.find(')', paren_open)
    if paren_close == -1:
        return line
    alt = line[bracket_open + 1:bracket_close]
    src = line[paren_open + 1:paren_close]
    return (
        line[:exclaim]
        + f'<img src="{src}" alt="{alt}" />'
        + line[paren_close + 1:]
    )