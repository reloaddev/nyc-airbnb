import plotly.express as px
from geopandas import GeoDataFrame
from shapely.geometry import Point
from data import df

geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
df = df.drop(['longitude', 'latitude'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)

def create_map():
    map = px.scatter_map(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=50,
        zoom=10
    )
    map.update_layout(height=1200)
    return map