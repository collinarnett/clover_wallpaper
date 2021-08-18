:four_leaf_clover: clover_wallpaper
==================
[![Build Status](https://travis-ci.com/collinarnett/clover_wallpaper.svg?branch=master)](https://travis-ci.com/collinarnett/clover_wallpaper)

cloverwallpaper makes it simple to fetch all images on a 4chan board for a specified resolution, making it ideal for finding wallpapers.

Installation
---------------

### Dependencies

cloverwallpaper requires:
 
 - python (>= 3.6)
 - tqdm
 - requests
---
### User installation


#### Python
```bash
pip install cloverwallpaper
```
#### Docker
```bash
docker run -v "$(pwd)":/home/cloverwallpaper collinarnett/cloverwallpaper:latest ARGUMENTS
```
---
Usage
---
```
usage: cloverwallpaper [-h] --boards BOARDS [BOARDS ...] --width WIDTH
                       --height HEIGHT
optional arguments:
  -h, --help            show this help message and exit
  --boards BOARDS [BOARDS ...]
                        target board to scrape images from
  --width WIDTH         width of the images you wish to download
  --height HEIGHT       height of the images you wish to download
```

