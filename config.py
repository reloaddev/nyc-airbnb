color_mapping_nyc = {
    'Bronx': '#f6b26b',
    'Brooklyn': '#76a5af',
    'Manhattan': '#c27ba0',
    'Queens': '#e06666',
    'Staten Island': '#93c47d',
    'New York City': '#9db59f'
}

color_mapping_bronx = {
    'Wakefield': '#f6b26b',
    'Mott Haven': '#f7b77a',
    'Williamsbridge': '#f9bc89',
    'Kingsbridge': '#f9c198',
    'Fordham': '#fac6a7',
    'Clason Point': '#fbcbb6',
    'Allerton': '#fcd0c5',
    'Concourse': '#fdd5d4',
    'Longwood': '#feddde',
    'Claremont Village': '#ffe3ec',
    'Other': '#fff0f2'
}

color_mapping_brooklyn = {
    'Bedford-Stuyvesant': '#678f98',
    'Williamsburg': '#7faab1',
    'Bushwick': '#89b2b7',
    'Crown Heights': '#93bbbd',
    'East Flatbush': '#9dc3c3',
    'Greenpoint': '#a8cbca',
    'Flatbush': '#b2d4d0',
    'East New York': '#bcdcd6',
    'Other': '#c7e5dc'
}

color_mapping_manhattan = {
    'Harlem': '#b57196',  # Darker shade
    'Midtown': '#bb789c',
    'Hell\'s Kitchen': '#c881a5',
    'Upper East Side': '#cd88ab',
    'Upper West Side': '#d290b1',
    'East Village': '#d89cb8',
    'East Harlem': '#dea4be',
    'Chelsea': '#e3abbf',
    'Lower East Side': '#e9b2c4',
    'Washington Heights': '#efbac9',
    'Other': '#f4c4cf',  # Lightest shade
}

color_mapping_queens = {
    'Astoria': '#c75c5c',  # Darker shade
    'Flushing': '#cd6464',
    'Long Island City': '#d56d6d',
    'Jamaica': '#dd7575',
    'East Elmhurst': '#e57e7e',
    'Woodside': '#e88787',
    'Ridgewood': '#eb9090',
    'Elmhurst': '#ee9a9a',
    'Sunnyside': '#f1a3a3',
    'Jackson Heights': '#f4adad',
    'Ditmars Steinway': '#f7b7b7',
    'Other': '#fac1c1',  # Lightest shade
}

color_mapping_staten_island = {
    'Tompkinsville': '#84b472',  # Darker shade
    'St. George': '#8bba76',
    'West Brighton': '#92c17a',
    'Mariners Harbor': '#99c87f',
    'Grant City': '#a1cf83',
    'Stapleton': '#a8d588',
    'Arrochar': '#aedc8c',
    'Shore Acres': '#b5e391',
    'Randall Manor': '#bcea95',
    'Clifton': '#c4f199',
    'New Brighton': '#cbf79e',
    'Other': '#d2fda2',  # Lightest shade
}

def get_colors_for_neighborhood_group(group):
    if group == 'Bronx':
        return color_mapping_bronx
    elif group == 'Brooklyn':
        return color_mapping_brooklyn
    elif group == 'Manhattan':
        return color_mapping_manhattan
    elif group == 'Queens':
        return color_mapping_queens
    elif group == 'Staten Island':
        return color_mapping_staten_island
    else:
        return color_mapping_nyc


def get_trendline_color_for_neighborhood_group(group):
    if group == 'Bronx':
        return '#094d94'
    elif group == 'Brooklyn':
        return '#895a50'
    elif group == 'Manhattan':
        return '#3d8460'
    elif group == 'Queens':
        return '#1f9999'
    elif group == 'Staten Island':
        return '#6c3b82'
    else:
        return '#624a60'




