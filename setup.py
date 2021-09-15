
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["PySimpleGUI>=4.0.0", "xlwings>=0.24.0", "openpyxl>=3.0.0"]

setup(
    name="notebookc",
    version="0.0.1",
    author="Jeff Hale",
    author_email="jeffmshale@gmail.com",
    description="A package to convert your Jupyter Notebook",
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