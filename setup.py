
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["PySimpleGUI>=4.0.0", "xlwings>=0.24.0", "openpyxl>=3.0.0", 
        "numpy>=1.20.0", "jellyfish>=0.8.8"]

setup(
    name="Excelutilities",
    version="0.0.4",
    author="Ethan Horsfall",
    author_email="ethan.horsfall@gmail.com",
    description="Useful functions for writing code for Excel applications",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/EthanTheMathmo/excel-utilities/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)