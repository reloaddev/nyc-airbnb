from dash import dcc
from data import df


def create_area_select():
    return dcc.Dropdown(
        id="area-select",
        value="New York City",
        options=[{"label": "New York City", "value": "New York City"}]
                + [{"label": group, "value": group}
                   for group in list(sorted(df["neighbourhood_group"].unique()))
                   ],
        placeholder="Select a Neighbourhood Group",
    )
