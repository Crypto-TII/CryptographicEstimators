# This is a custom-made Sphinx extension used to properly render
# kwargs in our HTML documentation.
# Its main purpose is to give meaning to nested indentation inside
# the "**kwargs" parameter of our docstrings, so we can document 
# what named arguments can be passed to any class, method or function.


def setup(app):
    print("kwargs_formatter extension is being loaded")
    # Connect the process_docstring function to the 'autodoc-process-docstring' event
    app.connect('autodoc-process-docstring', process_docstring)
    return {'version': '0.1', 'parallel_read_safe': True}

# This function will be applied to EVERY docstring collected by Sphinx 
# during the HTML docs generation.
def process_docstring(app, what, name, obj, options, lines):
    kwargs_start = 0
    kwargs_end = 0
    searching_for_kwargs = False
    # Find the start and end of the kwargs block by its indentation
    for i, line in enumerate(lines):
        if ':param \\*\\*kwargs:' in line and lines[i+1]:
            kwargs_start = i+1
            searching_for_kwargs = True
            continue
        if searching_for_kwargs and not line_has_indentation(line):
            kwargs_end = i
            searching_for_kwargs = False
    # Apply formatting if kwargs block is found
    if kwargs_start < kwargs_end:
        lines[kwargs_start:kwargs_end] = format_kwargs(lines[kwargs_start:kwargs_end])

def format_kwargs(lines):
    kwarg_param_indent = " "*4 # how much indentation we need for a proper kwarg rendering
    formatted_lines = ['']
    base_indentation = len(lines[0]) - len(lines[0].lstrip())
    for line in lines:
        if line.strip() == "": # skip empty lines
            continue
        deindented_line = line[base_indentation:]
        # if we reach a line without indentation (after base-deintented it), it's a new kwarg
        if not line_has_indentation(deindented_line):
            # Format parameter and description
            kwarg_parameter, kwarg_description = deindented_line.split(':', 1)
            formatted_lines.append(f'{kwarg_param_indent}**{kwarg_parameter.strip()}** - {kwarg_description.strip()}')
            formatted_lines.append('')
        else: 
            # Otherwise, append the description continuation to the previous kwarg
            formatted_lines[-2] += (f' {deindented_line.strip()}')

    return formatted_lines

def line_has_indentation(line):
    # Check if the line has leading whitespace
    return len(line.lstrip()) != len(line)
