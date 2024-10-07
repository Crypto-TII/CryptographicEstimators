def setup(app):
    print("kwargs_formatter extension is being loaded")
    app.connect('autodoc-process-docstring', process_docstring)
    return {'version': '0.1', 'parallel_read_safe': True}

def process_docstring(app, what, name, obj, options, lines):
    formatted_lines = format_kwargs(lines)
    lines[:] = formatted_lines

def format_kwargs(lines):
    formatted_lines = []
    in_kwargs = False
    kwargs_items = []

    for line in lines:
        if ':param \\*\\*kwargs:' in line:
            in_kwargs = True
            formatted_lines.append(line)
        elif in_kwargs and line.strip():
            kwargs_items.append(line.strip())
        else:
            if in_kwargs and kwargs_items:
                formatted_lines.append('')  # Add a blank line
                for item in kwargs_items:
                    key, value = item.split(':', 1)
                    formatted_lines.append(f'    {key.strip()} - {value.strip()}')
                    formatted_lines.append('')
                formatted_lines.append('')
                kwargs_items = []
            in_kwargs = False
            formatted_lines.append(line)

    # Handle case where kwargs are at the end of the docstring
    if in_kwargs and kwargs_items:
        formatted_lines.append('')
        for item in kwargs_items:
            key, value = item.split(':', 1)
            formatted_lines.append(f'    {key.strip()}')
            formatted_lines.append(f'        {value.strip()}')
        formatted_lines.append('')

    return formatted_lines
