from dash import html
from config import color_mapping_nyc


def get_legend():
    return html.Legend(
        html.Div([
            _get_legend_item("New York City", color_mapping_nyc.get("New York City")),
            _get_legend_item("Bronx", color_mapping_nyc.get("Bronx")),
            _get_legend_item("Brooklyn", color_mapping_nyc.get("Brooklyn")),
            _get_legend_item("Manhattan", color_mapping_nyc.get("Manhattan")),
            _get_legend_item("Queens", color_mapping_nyc.get("Queens")),
            _get_legend_item("Staten Island", color_mapping_nyc.get("Staten Island")),
        ] , style={"width": "50%", "display": "flex", "justify-content": "space-between"})
    )

def _get_legend_item(neighbourhood_group, color):
    return html.Div([
        html.Div("⬤", style={"color": color}),
        html.Div(neighbourhood_group, style={"font-size": "12px", "margin-left": "5px"}),
    ], style={"display": "flex", "align-items": "center"})
