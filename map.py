import pandas as pd
import plotly.express as px
import json

with open("europe.geojson") as f:
    europe_geojson = json.load(f)

country_ids = [feature["properties"]["FIPS"] for feature in europe_geojson["features"]]
df = pd.DataFrame({"country_id": country_ids})

def get_map_figure():
    fig = px.choropleth(
        df,
        geojson=europe_geojson,
        featureidkey="properties.FIPS",
        color="country_id",
        locations="country_id",
        range_color=[0, 100],
        fitbounds="locations",
        projection="mercator",
        scope="europe"
    )
    fig.update_layout(
        height=1000,  # Increase height to make the map larger
        width=2000,  # Increase width for larger display
        coloraxis_showscale=False  # Hide the color scale
    )
    return fig

# Call the function to generate the map
fig = get_map_figure()
fig.show()