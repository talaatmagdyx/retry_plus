import os


def create_project_structure(project_name):
    # Define the directory structure based on the project name
    directories = [
        f"{project_name}_package/{project_name}",
        f"{project_name}_package/tests"
    ]

    # Define the files to be created based on the project name
    files = [
        f"{project_name}_package/{project_name}/__init__.py",
        f"{project_name}_package/{project_name}/{project_name}.py",
        f"{project_name}_package/tests/__init__.py",
        f"{project_name}_package/tests/test_{project_name}.py",
        f"{project_name}_package/setup.py",
        f"{project_name}_package/README.md",
        f"{project_name}_package/LICENSE",
        f"{project_name}_package/requirements.txt"
    ]

    # Create the directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create the files
    for file in files:
        with open(file, 'w') as f:
            pass  # Just create an empty file

    # Add some basic content to the setup.py and README.rst
    setup_content = f"""from setuptools import setup, find_packages

setup(
    name='{project_name}',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={{
        'console_scripts': [
            # Add any console scripts here
        ],
    }},
)
"""

    readme_content = f"""# {project_name.capitalize()} Package

This is a Python package for {project_name} operations.
"""

    with open(f"{project_name}_package/setup.py", 'w') as f:
        f.write(setup_content)

    with open(f"{project_name}_package/README.md", 'w') as f:
        f.write(readme_content)

    print(f"Project structure for '{project_name}' created successfully.")


# Example usage
project_name = input("Enter the project name: ")
create_project_structure(project_name)
