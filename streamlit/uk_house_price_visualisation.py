import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from config.db_config import load_db_config
from utils.db_utils import get_db_connection
# from config.env_config import setup_env


# Set the title of the app
st.title("2025 England house prices Explorer")

# # Load the house price dataset
# data_file_path = 'etl/data/processed/cleaned_house_price_data.csv'
# df = pd.read_csv(data_file_path)


@st.cache_data
def load_data():
    connection_details = load_db_config()["target_database"]
    connection = get_db_connection(connection_details)
    query = "SELECT * FROM c12de.demo_sam_uk_house_prices_2025"
    df = pd.read_sql(query, connection)
    connection.close()
    return df


df = []

with st.spinner("Please wait while data loads..."):
    # setup_env([0, 'dev']) # Remove to deploy on cloud
    try:
        df = load_data()
    except Exception as e:
        st.write('An error occurred while loading the data.')
        print(f'error loading data from database: {e}')

if df is not []:
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
        default=sorted(df["property_type"].unique()))  # Sort default options

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

    # Add explanations of house price categories
    st.write('Category specification:')
    st.table([['Cheap', 'Affordable', 'Mid-range', 'High-end',
               'Millionaire Territory', 'Absolute Unit'],
              ['0 - 250k', '250k - 500k', '500k - 750k', '750k - 1m',
               '1m - 10m', '10m +']])

    # Create average house price by district map
    # With geo data from: https://martinjc.github.io/UK-GeoJSON/
    average_prices = filtered_df.groupby(
        "district")["price"].mean().reset_index()

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
