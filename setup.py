from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='retry_plus',
    version='1.0.1',
    description='A generic retry package for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Talaat Magdy',
    author_email='talaatmagdy75@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'pytest-asyncio',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
