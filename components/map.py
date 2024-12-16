from dash import Input, Output, callback
import plotly.express as px
from config import color_mapping
from geopandas import GeoDataFrame
from shapely.geometry import Point
from data import df
import pandas as pd

percentage_threshold = 0.03
geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
df = df.drop(['longitude', 'latitude'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)


def create_map():
    created_map = px.scatter_map(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        color_discrete_map=color_mapping,
        color='neighbourhood_group',
        size_max=50,
        zoom=10
    )
    created_map.update_layout(height=1200)
    return created_map


@callback(
    Output('interactive-map', 'figure'),
    Input('area-select', 'value')
)
def update_map(selected_area):
    if selected_area == "New York City":
        return create_map()
    filtered_data = gdf[gdf['neighbourhood_group'] == selected_area].copy()
    filtered_data.loc[:, 'percentage'] = (filtered_data.groupby('neighbourhood')['neighbourhood'].transform('count') / len(filtered_data))
    neighbourhoods_below_threshold = filtered_data.loc[
    filtered_data['percentage'] < percentage_threshold, 'neighbourhood'].unique()
    other_total_count = filtered_data.loc[
        filtered_data['neighbourhood'].isin(neighbourhoods_below_threshold), 'neighbourhood'].count()
    other_percentage = (
        filtered_data.loc[filtered_data['neighbourhood'].isin(neighbourhoods_below_threshold), 'percentage'].sum()
    )
    filtered_data = filtered_data[~filtered_data['neighbourhood'].isin(neighbourhoods_below_threshold)]
    if other_total_count > 0:
        other_row = pd.DataFrame({
            'neighbourhood': ['Other'],
            'percentage': [other_percentage],
            'calculated_host_listings_count': [other_total_count]
        })
        filtered_data = pd.concat([filtered_data, other_row], ignore_index=True)

    filtered_data = filtered_data[filtered_data['percentage'] >= percentage_threshold]
    created_map = px.scatter_map(
        filtered_data,
        lat=filtered_data.geometry.y,
        lon=filtered_data.geometry.x,
        color_continuous_scale=px.colors.cyclical.IceFire,
        color='neighbourhood',
        size_max=50,
        zoom=11
    )
    created_map.update_layout(height=1200)
    return created_map
