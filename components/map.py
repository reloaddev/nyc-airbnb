from dash import Input, Output, callback
import plotly.express as px
from geopandas import GeoDataFrame
from shapely.geometry import Point
from data import df

geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
df = df.drop(['longitude', 'latitude'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)


def create_map():
    created_map = px.scatter_map(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=50,
        zoom=10
    )
    created_map.update_layout(height=1200)
    return created_map


@callback(Output('interactive-map', 'figure'),
          Input('interactive-pie-chart', 'clickData'))
def update_map(click_data):
    if click_data:
        selected_group = click_data['points'][0]['label']
        filtered_data = gdf[gdf['neighbourhood_group'] == selected_group]
        created_map = px.scatter_mapbox(
            filtered_data,
            lat=filtered_data.geometry.y,
            lon=filtered_data.geometry.x,
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=50,
            zoom=10
        )
        created_map.update_layout(height=1200)
        return created_map
    else:
        return create_map()
