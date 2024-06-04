from setuptools import setup, find_packages

setup(
    name='retry',
    version='1.0.0',
    description='A generic retry package for Python',
    author='Talaat Magdy',
    author_email='talaatmagdy75@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'pytest-asyncio',
    ],
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
