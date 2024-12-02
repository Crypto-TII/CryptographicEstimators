def setup(app):
    print("kwargs_formatter extension is being loaded")
    app.connect('autodoc-process-docstring', process_docstring)
    return {'version': '0.1', 'parallel_read_safe': True}

def process_docstring(app, what, name, obj, options, lines):
    kwargs_start = 0
    kwargs_end = 0
    searching_for_kwargs = False
    # Extract the first and last line index of the kwargs indented block
    for i, line in enumerate(lines):
        if ':param \\*\\*kwargs:' in line and lines[i+1]:
            kwargs_start = i+1
            searching_for_kwargs = True
            continue
        if searching_for_kwargs and not line_has_indentation(line):
            kwargs_end = i
            searching_for_kwargs = False
    # If any kwargs block was found, apply the desired format
    if kwargs_start < kwargs_end:
        lines[kwargs_start:kwargs_end] = format_kwargs(lines[kwargs_start:kwargs_end])

def format_kwargs(lines):
    kwarg_param_indent = " "*4
    formatted_lines = ['']
    base_indentation = len(lines[0]) - len(lines[0].lstrip())
    for line in lines:
        if line.strip() == "":
            continue
        deindented_line = line[base_indentation:]
        if not deindented_line[0].isspace():
            kwarg_parameter, kwarg_description = deindented_line.split(':', 1)
            formatted_lines.append(f'{kwarg_param_indent}**{kwarg_parameter.strip()}** - {kwarg_description.strip()}')
            formatted_lines.append('')
        else: 
            formatted_lines[-2] += (f' {deindented_line.strip()}')

    return formatted_lines

def line_has_indentation(line):
    return len(line.lstrip()) != len(line)


