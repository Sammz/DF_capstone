# ![Digital Futures Academy](https://github.com/digital-futures-academy/DataScienceMasterResources/blob/main/Resources/datascience-notebook-header.png?raw=true)

## Digital Futures Data Engineering Academy Capstone Project
Author: Samuel Witt

This project extracts the UK house price paid data from the UK government website, transforms it and loads it into a database. A streamlit application uses this database to visualise UK house price statistics. 


### Dataset
Source of the data: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads

    Contains HM Land Registry data © Crown copyright and database right 2021.
    This data is licensed under the Open Government Licence v3.0.

Price Paid Data contains address data processed against Ordnance Survey’s AddressBase Premium product, which incorporates Royal Mail’s PAF® database (Address Data). Royal Mail and Ordnance Survey permit your use of Address Data in the Price Paid Data:

    - for personal and/or non-commercial use
    - to display for the purpose of providing residential property price information services

If you want to use the Address Data in any other way, you must contact Royal Mail. Email address.management@royalmail.com.

### User Stories 
```txt
USER STORY 1

As a Data Analyst,
I want to access a database with UK house price data,
So that I can create a streamlit app visualising UK house price data.
```

```txt
USER STORY 2

As a UK resident,
I want to select a street, postcode, city or region,
So that I can see the average, minimum and maximum house prices in that location.
```