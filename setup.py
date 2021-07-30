from setuptools import find_packages, setup


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='utilities',
    packages=find_packages(),
    version='0.0.1',
    description='Paquete de utilidades',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Juan Sebastián Martínez Serna',
)

