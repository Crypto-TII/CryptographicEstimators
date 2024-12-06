import os
from shutil import copyfile
from pathlib import Path

EXCLUDED_FOLDERS = ["__pycache__"]
EXCLUDED_FILES = ["__init__.py", "mq_main.sage.py",
                  "references.rst", "scipy_model.py"]
EXCLUDED_EXTENSIONS = [".md", ".so", ".dylib", ".egg-info", ".pyc", ".sage"]
SOURCE_ROOT_FOLDER = "./docs/source/"
Path(SOURCE_ROOT_FOLDER).mkdir(exist_ok=True)


def header_style(section, level):
    if not section:
        return ""

    sections = {
        0: "=",
        1: "-",
        2: "=",
        3: "-",
        4: "`",
        5: "'",
        6: ".",
        7: "~",
        8: "*",
        9: "+",
        10: "^"
    }
    style = sections[level] * len(section)

    if level in [0, 1]:
        return style + "\n" + section + "\n" + style + "\n"

    if level in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
        return section + "\n" + style + "\n"

    return section


with Path(SOURCE_ROOT_FOLDER, "index.rst").open(mode="w") as index_rst_file:
    index_rst_file.write("================================\n"
                         "CryptographicEstimators Library\n"
                         "================================\n"
                         "\n"
                         "This is a sample reference manual for CryptographicEstimators library.\n"
                         "\n"
                         "To use this module, you need to import it:: \n\n"
                         "    from cryptographic_estimators import *\n\n"
                         "This reference shows a minimal example of documentation of the\n"
                         "CryptographicEstimators library following SageMath guidelines.\n")

    ROOT_FOLDER = 'cryptographic_estimators/'

    for root, directories, files in os.walk(ROOT_FOLDER):
        path = root.split(os.sep)
        folder_name = os.path.basename(root).replace("_", " ")
        if os.path.basename(root) not in EXCLUDED_FOLDERS:
            rst_folder = root.replace(ROOT_FOLDER, SOURCE_ROOT_FOLDER)
            Path(rst_folder).mkdir(exist_ok=True)
            index_rst_file.write(
                f"{header_style(folder_name, len(path) - 1)}\n")
            index_rst_file.write(".. toctree::\n\n")
            for file in files:
                file_name = os.path.splitext(file)[0]
                file_extension = os.path.splitext(file)[1]
                if file not in EXCLUDED_FILES and file_extension not in EXCLUDED_EXTENSIONS:
                    file_without_extension = os.path.splitext(file)[0]
                    file_path = os.path.join(root, file_without_extension)
                    index_rst_file.write(
                        f"    {file_path.replace(ROOT_FOLDER, '')}\n")
                    with Path(rst_folder, file_name + ".rst").open(mode="w") as rst_file:
                        file_header = file_name.replace("_", " ")
                        adornment = "=" * len(file_header)
                        link = file_path.replace("/", ".")
                        rst_file.write(f"{header_style(file_name, 1)}\n"
                                       f".. automodule:: {link}\n"
                                       "   :members:\n"
                                       "   :undoc-members:\n"
                                       "   :inherited-members:\n"
                                       "   :show-inheritance:\n\n")
            index_rst_file.write(f"\n")

    index_rst_file.write("\n\n"
                         "General Information\n"
                         "===================\n"
                         "\n"
                         "* :ref:`Bibliographic References <references>`\n"
                         "\n"
                         "Indices and Tables\n"
                         "==================\n"
                         "\n"
                         "* :ref:`genindex`\n"
                         "* :ref:`modindex`\n"
                         "* :ref:`search`\n")

copyfile("conf.py", Path(SOURCE_ROOT_FOLDER, "conf.py"))
copyfile("references.rst", Path(SOURCE_ROOT_FOLDER, "references.rst"))
copyfile("docs/kwargs_formatter.py", Path(SOURCE_ROOT_FOLDER, "kwargs_formatter.py"))
