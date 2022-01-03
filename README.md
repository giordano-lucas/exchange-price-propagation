<img width="1665" alt="Screenshot 2021-12-29 at 09 52 48" src="https://user-images.githubusercontent.com/43466781/147644243-f21b52b6-bb45-42fe-848f-7c7f1222646c.png">


Exchange Price Propagation Analysis

======

## Abstract



## Research questions

1. 

## Proposed datasets

1. [Microsoft](https://disco.ethz.ch/misc/uniswap/cycles_in_Uniswap.json) XXX.


## Methods :

## Timeline and contributions :

### Week 1 : Data Acquisition & Setup (1)

| Task                                                                    | Team member(s)                  | work hours  |
| :-----------------------------------------------------------------------|:--------------------------------| -----------:|
| Literature research                                                     | Lucas & Augustin                | 3h          |
| API choice and query design                                             | Lucas & Augustin                | 4h          |
| EPFL Cluster & environment setup                                        | Lucas                           | 2h          |
| Data fetching script test                                               | Augustin                        | 3h          |
| Data fetching validation                                                | Augustin                        | 1h          |
| Data fetching improvements                                              | Augustin                        | 2h          |

### Week 4 : Clustering analysis, Profitablity prediction & report writing

| Task                                    | Team member(s)                  | work hours  |
| :---------------------------------------|:--------------------------------| -----------:|
|  Analysis                               | Lucas                           | 4h          |
| Profitablity prediction setup           | Augustin                        | 2h          |
| Github pages setup                      | Lucas                           | 2h          |
| Data story (1)                          | Lucas                           | 3h          |

### Week 5 : Hyperparameter opmisation and improvements & report writing

| Task                                    | Team member(s)                  | work hours  |
| :---------------------------------------|:--------------------------------| -----------:|
| Hyperparameter optmisation              | Lucas & Augustin                | 2h          |
| Notebook comments and markdown          | Lucas & Augustin                | 3h          |
| Data story (2)                          | Lucas & Augustin                | 6h          |

### Total contribution:

| Team member                     | work hours   |
|:--------------------------------| ------------:|
| Lucas Giordano                  | 38h          |
| Augustin Kapps                  | 35h          |


## Notes to the reader
### Organisation of the repository

In order to be able to run our notebook, you should have a folder structure similar to:

    .
    ├── data                                      # Data folder
    │ ├── diabetes_estimates_osward_2016.csv      # [Diabetes estimates Osward](https://drive.google.com/drive/folders/19mY0rxtHkAXRuO3O4l__S2Ru2YgcJVIA)
    │ ├── all                                     # folder containing [Tesco grocery 1.0](https://figshare.com/articles/Area-level_grocery_purchases/7796666)
    │ │  ├── Apr_borough_grocery.csv              # example of file
    │ │  ├── ...
    │ ├── statistical-gis-boundaries-london       # folder containing the unzipped [Statistical GIS Boundary Files for London](https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london) 
    │ │  ├── ESRI                                 # contains the data to be loaded by geopandas
    │ │  │  ├── London_Borough_Excluding_MHW.dbf  # example of file
    │ │  │  ├── ...
    │ │  ├── ...
    ├── images                              # Contains the ouput images and html used for the data story
    ├── extension.ipynb                     # Deliverable notebook for our extension
    ├── vizu.ipynb                          # Notebook containing only the vizualisations (if the reader only was to see the interactive viz)
    ├── Data Extraction.ipynb               # Notebook that generates the subset of tesco used in this analysis
    └── README.md               
    
Regarding the data folder a zip file can be downloaded [here](https://drive.google.com/drive/folders/1DH7EXo6Pbm2guJkWW75-wbYPa_5KTGQd?usp=sharing). It only remains to place it under the root directory of the repository and unzip it to be able to run the following notebooks. 


### Dependencies requirement

In the repository, we provide a `requirement.txt` file from which you can create a virutatal python environment.

