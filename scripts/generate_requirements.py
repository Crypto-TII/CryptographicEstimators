import toml
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one directory to reach the project root
project_root = os.path.dirname(script_dir)

# Paths for pyproject.toml and requirements.txt
pyproject_path = os.path.join(project_root, 'pyproject.toml')
requirements_path = os.path.join(project_root, 'requirements.txt')

# Read pyproject.toml
with open(pyproject_path, 'r') as f:
    pyproject = toml.load(f)

# Extract dependencies
dependencies = pyproject.get('project', {}).get('dependencies', [])

# Write to requirements.txt
with open(requirements_path, 'w') as f:
    for dep in dependencies:
        if not dep.startswith('#'):  # Skip commented out dependencies
            f.write(f"{dep}\n")

            #
