import os

COPYRIGHT = "# ****************************************************************************\n" + \
    "# Copyright 2023 Technology Innovation Institute\n" + \
    "#\n" + \
    "# This program is free software: you can redistribute it and/or modify\n" + \
    "# it under the terms of the GNU General Public License as published by\n" + \
    "# the Free Software Foundation, either version 3 of the License, or\n" + \
    "# (at your option) any later version.\n" + \
    "#\n" + \
    "# This program is distributed in the hope that it will be useful,\n" + \
    "# but WITHOUT ANY WARRANTY; without even the implied warranty of\n" + \
    "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n" + \
    "# GNU General Public License for more details.\n" + \
    "#\n" + \
    "# You should have received a copy of the GNU General Public License\n" + \
    "# along with this program.  If not, see <https://www.gnu.org/licenses/>.\n" + \
    "# ****************************************************************************"

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
                # if COPYRIGHT in file_content:
                #     print("copyright already in file", current_file_path)
                if COPYRIGHT not in file_content:
                    current_file.write(f'{COPYRIGHT}\n\n{file_content}')
                    current_file.truncate()
