import pandas as pd


def filter_by_neighbourhood_group(df, neighbourhood_group, threshold):
    """
    Filters data by neighbourhood group.
    Neighbourhoods below the threshold are grouped into "Other".
    Parameters:
        df: pandas DataFrame             - the data to filter
        neighbourhood_group: str         - the neighbourhood group to filter by
        threshold: float                 - the percentage threshold to filter by
    Returns:
        filtered_data: pandas DataFrame  - filtered data of neighbourhoods of neighbourhood_group
    """
    filtered_data = df[df['neighbourhood_group'] == neighbourhood_group].copy()

    # Step 1: Calculate percentage for each neighbourhood
    filtered_data.loc[:, 'percentage'] = (
            filtered_data.groupby('neighbourhood')['neighbourhood'].transform('count') / len(filtered_data)
    )

    # Step 2: Identify neighbourhoods below percentage_threshold
    neighbourhoods_below_threshold = filtered_data.loc[
        filtered_data['percentage'] < threshold, 'neighbourhood'].unique()

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

    return filtered_data[filtered_data['percentage'] >= threshold]
