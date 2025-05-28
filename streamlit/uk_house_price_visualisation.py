import streamlit as st
import plotly.express as px
import geopandas as gpd
from etl.extract.extract import extract_data
from etl.transform.transform import transform_data


# Set the title of the app
st.title("2025 England house prices Explorer")

# # Load the house price dataset
# data_file_path = 'etl/data/processed/cleaned_house_price_data.csv'
# df = pd.read_csv(data_file_path)

with st.spinner("Please wait while data loads..."):
    # Load the data from the internet for deployment
    print("Extracting data...")
    extracted_data = extract_data()
    print("Data extraction complete.")

    print("Transforming data...")
    transformed_data = transform_data(extracted_data)
    print("Data transformation complete.")

    df = transformed_data

# Show data
st.write("Here is a preview of the data:")
st.dataframe(df.head(5))

# Postcode input
postcode = st.text_input("Enter a postcode").strip().upper()

if postcode:
    matched = df[df['postcode'] == postcode]

    if not matched.empty:
        average_price = matched['price'].mean()
        st.success(f"Average house price in 2025 for {postcode}: £{int(
            average_price)}")
        st.dataframe(matched[['price', 'property_type', 'full_address']])
    else:
        st.warning("No data found for that postcode.")


# city input
city = st.text_input("Enter a city").strip().upper()

if city:
    matched = df[df['city'] == city]

    if not matched.empty:
        average_price = matched['price'].mean()
        # Capitalise just the first letter
        city = city[0] + city[1:].lower()
        st.success(f"Average house price in 2025 for {city}: £{int(
            average_price)}")
        st.dataframe(matched[['price', 'property_type', 'full_address']])
    else:
        st.warning("No data found for that city.")

# Add a sidebar for filters
st.sidebar.header("Filters for the graphs")
# Property type filter
property_filter = st.sidebar.multiselect(
    "Select Property type",
    options=sorted(df["property_type"].unique()),  # Sort the options
    default=sorted(df["property_type"].unique()))  # Sort the default options

# House age filter
house_age_filter = st.sidebar.multiselect(
    "Select house age",
    options=sorted(df["newbuild"].unique()),  # Sort the options
    default=sorted(df["newbuild"].unique()))  # Sort the default options

# duration filter
duration_filter = st.sidebar.multiselect(
    "Select Leasehold / Freehold",
    options=sorted(df["duration"].unique()),  # Sort the options
    default=sorted(df["duration"].unique()))  # Sort the default options

# Filter the DataFrame based on the selected filters
filtered_df = df[
    (df["property_type"].isin(property_filter)) &
    (df["newbuild"].isin(house_age_filter)) &
    (df["duration"].isin(duration_filter))]


category_counts = filtered_df[
    'house_price_category'].value_counts().reset_index()
category_counts.columns = ['house_price_category', 'count']

fig = px.bar(
    category_counts,
    x='house_price_category',
    y='count',
    title='Number of Properties by House Price Category',
    labels={'house_price_category': 'Category',
            'count': 'Number of Properties'},
    text='count')

st.plotly_chart(fig)

st.table([['Affordable', 'Cheap', 'Mid-range', 'High-end',
           'Millionaire Territory', 'Absolute Unit'],
          ['0 - 250k', '250k - 500k', '500k - 750k', '750k - 1m',
           '1m - 10m', '10m +']])


# Create average house price by district map
# With geo data from: https://martinjc.github.io/UK-GeoJSON/
average_prices = filtered_df.groupby("district")["price"].mean().reset_index()


geo_data_file = 'geodata/geojson_data.json'
geo_data = gpd.read_file(geo_data_file)

geo_data["district"] = geo_data["LAD13NM"].str.upper()
average_prices["district"] = average_prices["district"].str.upper()

# Left merge to ensure all locations are preserved, even if not all
# districts have house price data
geo_merged = geo_data.merge(average_prices, on="district", how="left")

# Change districts with missing data to -100000,
# such that they show up more distinctly white on the map
geo_merged["price"] = geo_merged["price"].fillna(-100000)

fig = px.choropleth(
    geo_merged,
    geojson=geo_merged.geometry,
    locations=geo_merged.index,
    title="England Average House Prices by District in 2025",
    color="price",
    color_continuous_scale="Reds",
    hover_name="district",
    hover_data={"price": ":,.0f"},
)

# Only display the districts with data, not the whole empty world
fig.update_geos(fitbounds="locations", visible=False)


st.plotly_chart(fig, use_container_width=True)
