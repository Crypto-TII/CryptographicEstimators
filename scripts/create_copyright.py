import os

COPYRIGHT = "# ****************************************************************************\n" + \
"# \t\tCopyright 2023 Technology Innovation Institute\n" + \
"# \n" + \
"# \tThis program is free software: you can redistribute it and/or modify\n" + \
"# \tit under the terms of the GNU General Public License as published by\n" + \
"# \tthe Free Software Foundation, either version 3 of the License, or\n" + \
"# \t(at your option) any later version.\n" + \
"# \n" + \
"# \tThis program is distributed in the hope that it will be useful,\n" + \
"# \tbut WITHOUT ANY WARRANTY; without even the implied warranty of\n" + \
"# \tMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n" + \
"# \tGNU General Public License for more details.\n" + \
"# \n" + \
"# \tYou should have received a copy of the GNU General Public License\n" + \
"# \talong with this program.  If not, see <https://www.gnu.org/licenses/>.\n" + \
"# ****************************************************************************\n "

ROOT_FOLDER = "cryptographic_estimators"
FILES_TO_READ = os.walk(ROOT_FOLDER)
EXCLUDED_FILES = ["__init__.py"]

for root, directories, files in FILES_TO_READ:
    for file in files:
        if file.endswith('.py') and file not in EXCLUDED_FILES:
            current_file_path = os.path.join(root, file)
            with open(current_file_path, 'r+') as current_file:
                file_content = current_file.read()
                current_file.seek(0, 0)
                if COPYRIGHT not in file_content:
                    current_file.write(f'{COPYRIGHT}\n\n{file_content}')
                    current_file.truncate()