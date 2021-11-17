# pharynx_detection

> 2020년 10월 ~ 2021년 04월<br>
> Data processing code for czi files

## 🖇️ Contents
- [pharynx_detection](#pharynx_detection)
  - [🖇️ Contents](#️-contents)
  - [💻 Stack](#-stack)
    - [Requirements](#requirements)
    - [install requirements](#install-requirements)
  - [💡 Features](#-features)
    - [1. Read `byte` from `.czi` file to export each frames into `.png` files](#1-read-byte-from-czi-file-to-export-each-frames-into-png-files)
    - [2. Delete error frame from exported files](#2-delete-error-frame-from-exported-files)
    - [3. Optional functions](#3-optional-functions)

## 💻 Stack
<p>
  <img src="https://img.shields.io/static/v1?label=&message=Python&color=blueviolet&logo=python&logoColor=FFFFFF"/>
  <img src="https://img.shields.io/static/v1?label=&message=opencv&color=3178C6&logo=opencv&logoColor=FFFFFF"/>
</p>

### Requirements

- python 3.6.5 ++
- argparse, numpy, cv2, natsort, tqdm

### install requirements

```
pip install --upgrade pip
pip install -r requirements.txt
```

## 💡 Features

### 1. Read `byte` from `.czi` file to export each frames into `.png` files
### 2. Delete error frame from exported files
### 3. Optional functions
  * Draw dots for validate exported files
  * Convert images into video for validate exported files
