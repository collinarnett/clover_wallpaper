#!/usr/bin/env python
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cloverwallpaper',
    packages=['cloverwallpaper'],
    version='0.2',
    description='A tool to download wallpapers from 4chan.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Collin Arnett',
    license='GPLv3',
    author_email='collin@arnett.it',
    url='https://github.com/collinarnett/clover_wallpaper',
    keywords=['4chan', 'wallpaper', 'downloader', 'image', 'scraper'],
    install_requires=[
        'requests',
        'tqdm',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6'
)
