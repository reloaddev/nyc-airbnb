from dash import Input, Output, callback
import plotly.express as px
from config import color_mapping
from data import df

# Remove outliers based on the Interquartile Range (IQR)
def filter_outliers(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return dataframe[(dataframe[column] >= lower_bound) & (dataframe[column] <= upper_bound)]

filtered_df = filter_outliers(df, 'price')


def create_violin_plot(data, title, color_key):
    return px.violin(
        data,
        x="price",
        box=True,
        points=None,
        title=title,
        labels={"price": "Price per night"},
        hover_data=["neighbourhood", "room_type"],
        color='neighbourhood_group' if color_key != "Overall" else None,
        color_discrete_sequence=[color_mapping["Overall"]] if color_key == "Overall" else None,
        color_discrete_map=color_mapping if color_key != "Overall" else None,
    )

@callback(
    Output('violin-plot', 'figure'),
    Input('neighbourhood-group-dropdown', 'value')
)
def update_violin_plot(selected_group):
    if selected_group:
        filtered_data = filtered_df[filtered_df['neighbourhood_group'] == selected_group]
        title = f"Price Distribution in {selected_group}"
    else:
        filtered_data = filtered_df
        title = "Overall Price Distribution"
        selected_group = 'Overall'  # Use 'Overall' color for combined data
    fig = create_violin_plot(filtered_data, title, selected_group)
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    return fig
