from dash import Input, Output, State, callback
import plotly.express as px
from data import df
from config import color_mapping
import pandas as pd


neighbourhood_group_data = df['neighbourhood_group'].value_counts().reset_index()
neighbourhood_group_data.columns = ['neighbourhood_group', 'calculated_host_listings_count']
neighbourhood_group_data['percentage'] = (neighbourhood_group_data['calculated_host_listings_count'] /
                                          neighbourhood_group_data['calculated_host_listings_count'].sum()) * 100


# Minimum percentage to include neighbourhood in pie chart
percentage_threshold = 0.03


def create_pie_chart():
    pie_chart = px.pie(
        neighbourhood_group_data,
        names='neighbourhood_group',
        values='percentage',
        title="Percentage of listings by Neighbourhood Group",
        labels={'percentage': '% Listings'},
        color='neighbourhood_group',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(textposition='outside', textinfo='percent+label')
    return pie_chart


@callback(
    Output('interactive-pie-chart', 'figure'),
    Input('area-select', 'value')
)
def update_pie_chart(selected_area):
    if selected_area == "New York City":
        return create_pie_chart()

    # Filter data for the selected area
    filtered_data = df[df['neighbourhood_group'] == selected_area].copy()  # Avoid SettingWithCopyWarning

    # Step 1: Calculate percentage for each neighbourhood
    filtered_data.loc[:, 'percentage'] = (
            filtered_data.groupby('neighbourhood')['neighbourhood'].transform('count') / len(filtered_data)
    )

    # Step 2: Identify neighbourhoods below percentage_threshold
    neighbourhoods_below_threshold = filtered_data.loc[filtered_data['percentage'] < percentage_threshold, 'neighbourhood'].unique()

    # Step 3: Sum all rows below percentage_threshold into "Other"
    other_total_count = filtered_data.loc[
        filtered_data['neighbourhood'].isin(neighbourhoods_below_threshold), 'neighbourhood'].count()
    other_percentage = (
        filtered_data.loc[filtered_data['neighbourhood'].isin(neighbourhoods_below_threshold), 'percentage'].sum()
    )

    # Remove neighbourhoods below percentage_threshold and add summed "Other" row
    filtered_data = filtered_data[~filtered_data['neighbourhood'].isin(neighbourhoods_below_threshold)]
    if other_total_count > 0:  # Only add "Other" if there are rows below percentage_threshold
        other_row = pd.DataFrame({
            'neighbourhood': ['Other'],
            'percentage': [other_percentage],
            'calculated_host_listings_count': [other_total_count]
        })
        filtered_data = pd.concat([filtered_data, other_row], ignore_index=True)

    # Step 4: Remove rows again below percentage_threshold (including "Other" if it's < percentage_threshold)
    filtered_data = filtered_data[filtered_data['percentage'] >= percentage_threshold]

    pie_chart = px.pie(
        filtered_data,
        names='neighbourhood',
        values='percentage',
        title=f"Percentage of listings in {selected_area} by Subgroup",
        labels={'percentage': '% Listings'},
        color='neighbourhood',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(textposition='outside', textinfo='percent+label')
    return pie_chart



