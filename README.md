# ![Digital Futures Academy](https://github.com/digital-futures-academy/DataScienceMasterResources/blob/main/Resources/datascience-notebook-header.png?raw=true)

## Digital Futures Data Engineering Academy Capstone Project
Author: Samuel Witt

This project extracts the 2025 UK house price paid data from the UK government website, transforms it and loads it into a database. A streamlit application uses this database to visualise 2025 residential UK house price statistics. 

---

### Dataset
Source of the data: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads

    Contains HM Land Registry data © Crown copyright and database right 2021.
    This data is licensed under the Open Government Licence v3.0.

Price Paid Data contains address data processed against Ordnance Survey’s AddressBase Premium product, which incorporates Royal Mail’s PAF® database (Address Data). Royal Mail and Ordnance Survey permit your use of Address Data in the Price Paid Data:

    - for personal and/or non-commercial use
    - to display for the purpose of providing residential property price information services

If you want to use the Address Data in any other way, you must contact Royal Mail. Email address.management@royalmail.com.

---

### User Stories
```txt
USER STORY 1

As a Data Analyst,
I want to access a database with cleaned UK house price data,
So that I can create a streamlit app visualising UK house price data.
```

```txt
USER STORY 2

As a UK resident,
I want to select my postcode or city,
So that I can see the average house prices in my location.
```
```txt
USER STORY 3

As a Home Buyer,
I want to filter by property type (e.g., Detached, Semi-Detached),
So that I can understand pricing for my preferred home style.
```

```txt
USER STORY 4

As a Developer,
I want the ETL pipeline to log successes and failures,
So that I can monitor and debug data ingestion reliably.

```

```txt
USER STORY 5

As a user,
I want to see a breakdown of house prices by category, 
so I can understand the housing market.
```
---

### Schema design
The cleaned dataset contains the following columns:
| transaction_id | price | date | postcode | property_type | newbuild | duration | PAON | SAON | street | locality | city | district | county | house_price_category | full_address |
|----------------|-------|------|----------|----------------|----------|----------|------|------|--------|----------|------|----------|--------|-----------------------|--------------|

For an explanation of the columns visit [Explanations of column headers](https://www.gov.uk/guidance/about-the-price-paid-data#explanations-of-column-headers-in-the-ppd)

I have renamed old/new to newbuild for clarity, and added the house_price_category and full_address columns to enrich the data.

The Record status and PPD Category Type columns have been removed, after filtering the data to consist of only single residential properties sold for value and A records.

---

### Installation
Please visit the [installation instructions](INSTALLATION.md).

---


###  Optimising query execution and performance
<!-- How would I go about optimising query execution and performance if the dataset continues to increase? -->
The full historical UK house price dataset currently contains [4.3GB](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#single-file) of transaction data. One could even think of including more countries and combining house price data from all over the world for analysis. To optimise query execution and performance I would propose to switch from Pandas to PySpark to handle the data. PySpark is known for its distributed computing across multiple cores or machines and is designed for large datasets. Instead of CSV files I would switch to using parquet files to leverage the benefits of storing data in a binary format. 

---

### Error handling and logging
<!-- What error handling and logging have you included in your code and how this could be leveraged? -->
In every step of the ETL pipeline the process is uses error handling and logging to create a streamlined experience. Errors are caught, handled and logged. This ensures that if anything goes wrong, it is easy to trace where in the pipeline it happened and understand how to fix the problem. Informative logging is utilised as well to give updates on what is happening and how long certain steps in the process take. For example the cleaning and enriching steps log an entry when completed with the amount of time they took to complete.

---

### Security or privacy issues

<!-- Are there any security or privacy issues that you need to consider and how would you mitigate them? -->
The dataset used in this project is a public dataset released by the government. I have mentioned their license and copyright notice in the README to comply with their use policy. Users of this project need to adhere to this policy as well. 

The streamlit app contains user input fields which need to be sanitised to prevent users from injecting malicious code to break the application or steal information. 

Users can input a postcode, and they might be likely to input their own postcode. To ensure their privacy, it is important to not log their IP address and postcode input, as these together could lead to identifiable information.

---

### How this project could be deployed or adapted into an automated cloud environment using the AWS services you have covered?
<!-- How this project could be deployed or adapted into an automated cloud environment using the AWS services you have covered? -->
To run this project in the AWS cloud environment, one could use the following services:

- Lambda to schedule downloading the monthly update of the government data to an S3 bucket
- S3 to store the raw downloaded csv files
- Use Step Functions to automate the pipeline
- Athena to create tables, insert data and query the data
- DynamoDB to store processed data in a table structure
- Quicksight to create a dashboard and visualisations