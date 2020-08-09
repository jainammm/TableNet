# TableNet

Unofficial implementation of ICDAR 2019 paper : _TableNet: Deep Learning model for end-to-end Table detection and Tabular data extraction from Scanned Document Images._ 

[__Paper__](https://arxiv.org/abs/2001.01469)

## Overview
**Paper: TableNet: Deep Learning model for end-to-end Table detection and Tabular data extraction from Scanned Document Images**

TableNet is a modern deep learning architecture that was proposed by a team from TCS Research year in the year 2019. The main motivation was to extract information from scanned tables through mobile phones or cameras.

They proposed a solution that includes accurate detection of the tabular region within an image and subsequently detecting and extracting information from the rows and columns of the detected table.

**Architecture:** The architecture is based out of Long et al., an encoder-decoder model for semantic segmentation. The same encoder/decoder network is used as the FCN architecture for table extraction. The images are preprocessed and modified using the Tesseract OCR. 

Source: [Nanonets](https://nanonets.com/blog/table-extraction-deep-learning/#tablenet?&utm_source=nanonets.com/blog/&utm_medium=blog&utm_content=Table%20Detection,%20Information%20Extraction%20and%20Structuring%20using%20Deep%20Learning)


![architecture](https://github.com/jainammm/TableNet/raw/master/architecture.png)

## How to run
```
pip install -r requirements.txt
```

1. Download the Marmot Dataset from the link given in readme.
1. Run `data_preprocess/generate_mask.py` to generate Table and Column Mask of corresponding images.
1. Follow the `TableNet.ipynb` notebook to train and test the model.

## Challenges
* Require a very decent System with a good GPU for accurate result on High pixel images. 

## Dataset

Download the dataset provided in paper : [Marmot Dataset](https://drive.google.com/drive/folders/1QZiv5RKe3xlOBdTzuTVuYRxixemVIODp). 
