# pharynx_detection

- 20.10 ~ 21.04
- Data preprocessing codes for pharnyx detection

## Requirements

- python 3.6.5 ++
- argparse, numpy, cv2, natsort, tqdm

### install requirements

```
pip install --upgrade pip
pip install -r requirements.txt
```

## Features

1. Read `byte` from `.czi` file to export each frames into `.png` files
2. Delete error frame from exported files
3. (optional) Draw dots for validate exported files
4. (optional) Convert images into video for validate exported files
