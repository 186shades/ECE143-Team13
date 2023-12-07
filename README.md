# Data Analysis for Solar Radiation

---
## Summary
This project focuses on understanding and analysis of solar supply and energy demand data. Data can be explored for multiple states, but focus of the analysis is on California state. It also explores the solar supply-demand gap in California with some assumptions for the California grid capacity and efficiency. 

---

## Data Source
1. National Renewable Energy Laboratory - National Solar Radiation Database https://nsrdb.nrel.gov/
2. California Independent System Operator - https://github.com/grgmiller/CAISO_data

---

## Installation

There are multiple ways to fetch the data from NSRDB website. 
To fetch the data provided from Amazon Web Services using the HDF Group's Highly Scalable Data Service (HSDS).

install h5pyd:

```
pip install --user h5pyd
```

configure HSDS:

```
hsconfigure
```

and enter at the prompt:

```
hs_endpoint = https://developer.nrel.gov/api/hsds
hs_username = None
hs_password = None
hs_api_key = 3K3JQbjZmWctY0xmIfSYvYgtIcM3CN0cb1Y2w9bf
```

*The example API key here is for demonstation and is rate-limited per IP. To get your own API key, visit https://developer.nrel.gov/signup/*

You can also add the above contents to a configuration file at ~/.hscfg

Another way to fetch the data is to directly download csv files from the NSRDB website using https://nsrdb.nrel.gov/data-viewer . 
We can specify data attributes as per our need but this has limited usage as there is download limitation on the size of the file.

---
## Code Structure:

### Project Jupyter Notebook:
- [Solar.ipynb](./notebooks/Solar.ipynb) has the following parts:
	1. Supply Visualization
 	2. Demand Visualization
  	3. Energy Visualization (Supply-Demand Gap Analysis)
  	4. Functionality and Coverage Testing
---

## File Structure:
1. [notebooks](./notebooks):
	- Contains the notebook [Solar.ipynb](./notebooks/Solar.ipynb) for analysis, visualizations, and testing
 	- Energy analysis code inside [Energy_Analysis.py](./notebooks/Energy_Analysis.py)
    - We fetched and analysed data for supply visualizations using the HSDS on the fly
    - For demand and gap analysis we preprocessed and downloaded the csv files as per our requirements
2. [raw_data](./raw_data/):
    - Our supply and demand data files used for gap analysis can be found here
3. [OutputImages](./raw_data/):
     - Contains the graphs and images generated from analysis

---

## Required Packages:
> h5pyd

> pandas

> numpy

> scipy

> matplotlib

> imageio

> datetime

> pytz

> pickle

---
