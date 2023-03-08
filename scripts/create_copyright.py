import os

COPYRIGHT = """
# Copyright 2023 
"""

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