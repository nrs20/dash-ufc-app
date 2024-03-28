import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dash

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import load_figure_template

df = pd.read_csv('masterdataframe.csv')

# IDEA: show the stats of the fighter inputted and put it on a second plot ORRRRRR have it passed in from the radioItem...or maybe even a checklist? idk
jon = df.loc[df['fighter'] == 'Jon Jones']

fighter_dropdown = df['fighter'].unique()
fighter_dropdown.sort()
column_names = df.columns

#drop specific columns from column_names
column_names = column_names.drop(['fighter_url','opponent_url','stance','date','opponent','division','method','event_url','reach','height','age','referee',"fight_url", "fighter","dob","time", "time_format","total_comp_time"])

#result == 1 means the fighter in the 'fighter' column won


# selects all rows where the fighter's stance is 'Orthodox'
# .loc[:, ['fighter', 'stance']]: After filtering rows where the stance is 'Orthodox',
# this part selects all rows (denoted by :) and only the columns 'fighter' and 'stance'.
# So, it retrieves the 'fighter' and 'stance' columns for the filtered rows.
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns

desired_divisions = ['Open Weight', 'Women\'s Strawweight', 'Women\'s Bantamweight', 'Women\'s Flyweight', 'Flyweight','Bantamweight','Featherweight','Lightweight','Welterweight','Middleweight','Light Heavyweight','Heavyweight']
division_filter = df[df['division'].isin(desired_divisions)]


#getting the fighters who have won's name, stance, and division
#basically the condition is the 'result'==1, then : gets all the rows, and ['fighter', 'stance', 'division'] gets the columns
winners = df.loc[df['result'] == 1].loc[:, ['fighter', 'stance', 'division','method','total_strikes_landed', 'knockdowns', 'age', 'height', 'reach','head_strikes_landed','total_strikes_accuracy', 'sig_strikes_accuracy','head_strikes_accuracy', 'distance_strikes_landed','takedowns_landed','head_strikes_landed', 'takedowns_def','total_strikes_def','leg_strikes_landed','clinch_strikes_landed','body_strikes_landed','ground_strikes_landed']]

losers = df.loc[df['result'] == 0].loc[:, ['fighter', 'stance', 'division']]

losers_grouped_by_division = losers.groupby('division')

# Create an empty dictionary to store the loser results
loser_division_results = {}

# Perform the query and store the results in the dictionary
for division, division_df in losers_grouped_by_division:
    loser_division_results[division] = division_df
    
    
winners_grouped_by_division = winners.groupby('division')
winner_division_results = {}
for division, division_df in winners_grouped_by_division:
    winner_division_results[division] = division_df


#get the number of unique fighters in each division
unique_fighters_per_division = df.groupby('division')['fighter'].nunique()

filtered_index = [division for division in unique_fighters_per_division.index if 'Open Weight' and 'Catch Weight' not in division]

reordered_index = unique_fighters_per_division.reindex(desired_divisions)

"""
show each fighter's win breakdown"""
#show each fighter's win breakdown in a pie chart
fighter_breakdown = df.loc[df['fighter'] == 'Max Holloway'].loc[:, ['result', 'method', 'age', 'total_strikes_landed', 'knockdowns']]

fighter_breakdown_wins = fighter_breakdown[fighter_breakdown['result'] == 1].value_counts()

# Create the Dash 
app = dash.Dash(external_stylesheets=[dbc.themes.MORPH], suppress_callback_exceptions=True, assets_folder="static")
#UNCOMMENT THIS BEFORE DEPLOYING, AND ALSO MOVE CSV FILE BACK INTO THE SRC FOLDER
server = app.server
load_figure_template("MORPH")  # Load the template
spinners = html.Div(
    [
        dbc.Spinner(size="sm"),
        html.Hr(),
        dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}),
    ]
)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "/static/pic1.png"},
        {"key": "2", "src": "/static/pic2.png"},
        {"key": "3", "src": "/static/pic3.png"},
        {"key": "4", "src": "/static/pic4.png"},
        {"key": "5", "src": "/static/pic5.png"},
    ],
    controls=False,
    indicators=False,
    interval=3000,
    ride="carousel",
    className="carousel-sm",  # Add this line to make the carousel smaller
        style={'display': 'flex', 'justify-content': 'center'}

    #make carousel centered
    
)

accordion = html.Div(
    [
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    "Differentials, such as reach_differential, height_differential, etc. are calculated by dividing the two individual's technique stats. For example, if Conor hits Khabib 10 times, and Khabib hits Conor 5 times, then Conor's differential stat is 10/5 = 2. Khabib's differential stat is 0.5.",
                    title="Differentials",
                    item_id="item-1",
                ),
                dbc.AccordionItem(
                    "Control is measured in seconds. If Khabib has 1 minute of control time in a fight, then his control stat is 60.",
                    title="Control",
                    item_id="item-2",
                ),
                dbc.AccordionItem(
                    "Accuracy is measured in percentages. If Conor lands 10 strikes out of 20, then his accuracy stat is 50%.",
                    title="Accuracy",
                    item_id="item-3",
                ),
                 dbc.AccordionItem(
                    "Precomp is a stat that measures the fighter's performance before the fight. For example, Jon Jones' precomp_avg_sig_strikes_landed would show his average stats for significant strikes landed before whichever fight you are observing.",
                    title="Precomp",
                    item_id="item-4",
                )
                 ,
                  dbc.AccordionItem(
                    "Result is a binary variable that shows whether the fighter won or lost the fight. 1 means the fighter won, 0 means the fighter lost.",
                    title="Result",
                    item_id="item-5",
                ),
                   dbc.AccordionItem(
                    "Both height and reach are measured in inches.",
                    title="Height & Reach",
                    item_id="item-6",
                )
            ],
            id="accordion",
            active_item="item-1",
        ),
        html.Div(id="accordion-contents", className="mt-3"),
    ]
)





# Define the layout
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-0', children=[
        dcc.Tab(label="Welcome", value='tab-0', children=[
            html.Div([
                html.H1("Welcome to the UFC Data Analysis Dashboard!", style={'textAlign': 'center'}),
                html.P("This dashboard provides insights such as UFC fighters' performance & career statistics, division finishes, and fighter stances.", style={'textAlign': 'center'}),
                 html.P("The data was gathered from Kaggle and contains thousands of entries starting from the first UFC event and going up to 2022.", style={'textAlign': 'center'}),
#display the link to this: https://www.kaggle.com/datasets/danmcinerney/mma-differentials-and-elo


  html.P([
            "Below are some examples of the data that can be visualized using this dashboard; click on the tabs above to explore the data further! ",
            html.A("Click here to access the dataset on Kaggle.", href="https://www.kaggle.com/datasets/danmcinerney/mma-differentials-and-elo", className="kaggle")
        ], style={'textAlign': 'center'}),
    ], style={'textAlign': 'center'}),  # Center the content horizontally            ]),
            carousel
        ]),
        dcc.Tab(label='Fighter Win Stat Breakdown', value='tab-1'),
        dcc.Tab(label='Division Finishes Breakdown', value='tab-6'),
        dcc.Tab(label='Fighter Stance Breakdown', value='tab-3'),
        dcc.Tab(label='Correlation Breakdown', value='tab-4'),
        dcc.Tab(label='Fighter Career Stats', value='tab-5'),
    dcc.Tab(label='About', value='tab-2', children=[html.Div([html.H1("Have a question about how a certain variable is calculated? Take a look below!")]) ,  accordion])
    ]),
    html.Div(id='tabs-content')
])


@app.callback(dash.dependencies.Output('tabs-content', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-0':
        return
        
    elif tab == 'tab-1':
        return html.Div([
            html.H1("Fighter Win Stat Breakdown", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='fighter-input',
                options=fighter_dropdown, 
                value='Conor McGregor'
            ),
 dbc.Spinner(
                dcc.Graph(id='pie-chart'),
                color="primary",
                type="grow",
            ),          
 dbc.RadioItems(
                id='radio-items',
                options=[
                    {'label': 'Wins', 'value': 1},
                    {'label': 'Losses', 'value': 0}
                ],
                value=1,            
                inline=True,

            )
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H1("Division Finishes Breakdown", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='division-dropdown',
                options=[
                    {'label': 'Women\'s Divisions', 'value': 'Women\'s'},
                    {'label': 'Men\'s Divisions', 'value': 'Men'},
                ],
                value='Men'
            ),
           dbc.Spinner(
                dcc.Graph(id='bar-chart'),
                color="primary",
                type="grow",
            ),
            dbc.RadioItems(
                id='radio-method',
               options=[
                    {'label': 'KO/TKO', 'value': 'KO/TKO'},
                    {'label': 'SUB', 'value': 'SUB'},
                    {'label': 'U-DEC', 'value': 'U-DEC'},
                    {'label': 'S-DEC', 'value': 'S-DEC'},
                    {'label': 'M-DEC', 'value': 'M-DEC'},
                    {'label': 'DQ', 'value': 'DQ'},
                ],
                value='KO/TKO', inline=True,
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H1("Fighter Stance Breakdown", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='div-dropdown',
                options=[
                    {'label': 'Women\'s Strawweight', 'value': 'Women\'s Strawweight'},
                    {'label': 'Women\'s Flyweight', 'value': 'Women\'s Flyweight'},
                    {'label': 'Women\'s Bantamweight', 'value': 'Women\'s Bantamweight'},
                    {'label': 'Flyweight', 'value': 'Flyweight'},
                    {'label': 'Bantamweight', 'value': 'Bantamweight'},
                    {'label': 'Featherweight', 'value': 'Featherweight'},
                    {'label': 'Lightweight', 'value': 'Lightweight'},
                    {'label': 'Welterweight', 'value': 'Welterweight'},
                    {'label': 'Middleweight', 'value': 'Middleweight'},
                    {'label': 'Light Heavyweight', 'value': 'Light Heavyweight'},
                    {'label': 'Heavyweight', 'value': 'Heavyweight'}
                ],
                value='Lightweight'
            ),
             dbc.Spinner(
            dcc.Graph(id='stance-chart', style={'textAlign': 'center'}),
                color="primary",
                type="grow",
            ),
            dbc.RadioItems(
                id='radio-stance',
                     options=[
                {'label': 'Total Strikes Landed', 'value': 'total_strikes_landed'},
                {'label': 'Body Strikes Landed', 'value': 'body_strikes_landed'},
                {'label': 'Leg Strikes Landed', 'value': 'leg_strikes_landed'},
                {'label': 'Clinch Strikes Landed', 'value': 'clinch_strikes_landed'},
                {'label': 'Ground Strikes Landed', 'value': 'ground_strikes_landed'},
                {'label': 'Knockdowns', 'value': 'knockdowns'},
                {'label': 'Takedowns Landed', 'value': 'takedowns_landed'},
                {'label': 'Takedowns Defended', 'value': 'takedowns_def'},
                {'label': 'Distance Strikes Landed', 'value': 'distance_strikes_landed'},
                {'label': 'Total Strikes Defended', 'value': 'total_strikes_def'},],
                value='knockdowns', inline=True,
            )
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H1("Correlation Breakdown", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='correlation-dropdown',
                    options=[
                         {'label': 'Women\'s Strawweight', 'value': 'Women\'s Strawweight'},
                    {'label': 'Women\'s Flyweight', 'value': 'Women\'s Flyweight'},
                    {'label': 'Women\'s Bantamweight', 'value': 'Women\'s Bantamweight'},
                {'label': 'Flyweight', 'value': 'Flyweight'},
                {'label': 'Bantamweight', 'value': 'Bantamweight'},
                {'label': 'Featherweight', 'value': 'Featherweight'},
                {'label': 'Lightweight', 'value': 'Lightweight'},
                {'label': 'Welterweight', 'value': 'Welterweight'},
                {'label': 'Middleweight', 'value': 'Middleweight'},
                {'label': 'Light Heavyweight', 'value': 'Light Heavyweight'},
                {'label': 'Heavyweight', 'value': 'Heavyweight'}
            ],
                value='Lightweight'
            ),
            dbc.Spinner(
             dcc.Graph(id='correlation-graph'),
                color="primary",
                type="grow",
            ),
        html.H2("Y-axis"),
        dbc.RadioItems(
            id='correlation-checklist-yaxis',
            options=[
                {'label': 'Height', 'value': 'height'},
                {'label': 'Reach', 'value': 'reach'},
                {'label': 'Total Strikes Landed', 'value': 'total_strikes_landed'},
                {'label': 'Total Strikes Accuracy', 'value': 'total_strikes_accuracy'},

                {'label': 'Body Strikes Landed', 'value': 'body_strikes_landed'},
                {'label': 'Leg Strikes Landed', 'value': 'leg_strikes_landed'},
                {'label': 'Clinch Strikes Landed', 'value': 'clinch_strikes_landed'},
                {'label': 'Ground Strikes Landed', 'value': 'ground_strikes_landed'},


                {'label': 'Knockdowns', 'value': 'knockdowns'},
                {'label': 'Takedowns Landed', 'value': 'takedowns_landed'},
                {'label': 'Takedowns Defended', 'value': 'takedowns_def'},

                {'label': 'Distance Strikes Landed', 'value': 'distance_strikes_landed'},
                {'label': 'Total Strikes Defended', 'value': 'total_strikes_def'},
            ],
            value='total_strikes_landed', inline=True,
                    style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'wrap'}

        ),
           html.H2("X-axis"),
        dbc.RadioItems(
            id='correlation-checklist',
            options=[
                {'label': 'Height', 'value': 'height'},
                {'label': 'Reach', 'value': 'reach'},
                {'label': 'Total Strikes Landed', 'value': 'total_strikes_landed'},
                {'label': 'Total Strikes Accuracy', 'value': 'total_strikes_accuracy'},

                {'label': 'Body Strikes Landed', 'value': 'body_strikes_landed'},
                {'label': 'Leg Strikes Landed', 'value': 'leg_strikes_landed'},
                {'label': 'Clinch Strikes Landed', 'value': 'clinch_strikes_landed'},
                {'label': 'Ground Strikes Landed', 'value': 'ground_strikes_landed'},

               
                {'label': 'Knockdowns', 'value': 'knockdowns'},
                {'label': 'Takedowns Landed', 'value': 'takedowns_landed'},
                {'label': 'Takedowns Defended', 'value': 'takedowns_def'},

                {'label': 'Distance Strikes Landed', 'value': 'distance_strikes_landed'},
                {'label': 'Total Strikes Defended', 'value': 'total_strikes_def'},
            ],
            value='reach', inline=True,
                                style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'wrap'}

        ),
               
    ])
    elif tab == 'tab-5':
        return html.Div([
            html.H1("Fighter Stats", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='fighter-stats-dropdown',
                options=fighter_dropdown, value='Conor McGregor'
            ),
            dcc.Dropdown(
                id='fighter-specify-stats-dropdown',
                options=column_names,
                value='total_strikes_landed'
            ),
              dbc.Spinner(
            dcc.Graph(id='fighter-full-stats-graph'),
                color="primary",
                type="grow",
            ),
        ])
    elif tab == 'tab-2':
        return
 
 
# Define the callback function, also listen for the change on radioItems

@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    

    [dash.dependencies.Input('fighter-input', 'value')],
            [dash.dependencies.Input('radio-items', 'value')],

    
)

def update_pie_chart( fighter_name, radio_items):
    if fighter_name and radio_items is not None:
        # Filter the data for the selected fighter
        fighter_breakdown = df.loc[df['fighter'] == fighter_name].loc[:, ['result', 'method']]

        if radio_items == 1:  # Filter for wins
            fighter_breakdown = fighter_breakdown[fighter_breakdown['result'] == 1]
            title = f"Winning Methods Breakdown for {fighter_name}"
        else:  # Filter for losses
            fighter_breakdown = fighter_breakdown[fighter_breakdown['result'] == 0]
            title = f"Losing Methods Breakdown for {fighter_name}"

        # Count the occurrences of each method
        fighter_breakdown_wins = fighter_breakdown['method'].value_counts().reset_index()
        fighter_breakdown_wins.columns = ['method', 'count']  # Rename columns

        # Create the pie chart
        fig = px.pie(fighter_breakdown_wins, names='method', values='count', title=title)
        return fig

    # Return an empty figure if no fighter name is provided or radio item is not selected
    return {}


@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('division-dropdown', 'value')],
    [dash.dependencies.Input('radio-method', 'value')],
)
def division_finishes_breakdown(selected_division, selected_method):
    if selected_division == 'Women\'s':
        desired_divisions = ['Women\'s Strawweight', 'Women\'s Bantamweight', 'Women\'s Flyweight']
    else:
        desired_divisions = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight']
    division_filter = df[df['division'].isin(desired_divisions)]
    division_method_counts = {}
    for division, division_df in winner_division_results.items():
        if division in desired_divisions:
            division_method_counts[division] = division_df['method'].value_counts().to_dict()
    # Initialize lists to hold division names and SUB finish counts
    divisions = []
    sub_finish_counts = []

    # Iterate over the dictionary to populate the lists
    for division, finishes in division_method_counts.items():
        if division not in ['Open Weight', 'Catch Weight', 'Super Heavyweight']:
            divisions.append(division)
            sub_finish_counts.append(finishes.get(selected_method, 0))
            
    # Combine divisions and their corresponding SUB finish counts into a list of tuples
    combined_data = list(zip(divisions, sub_finish_counts))
    # Create a DataFrame
    df_Div = pd.DataFrame(combined_data, columns=['Division', 'Count'])
    # Set the figure size for better readability
    
    #order the divisions by the count of the selected method
    df_Div = df_Div.sort_values(by='Count', ascending=False)
    
    fig = px.bar(df_Div, x="Count", y='Division', title=f'{selected_method} Count by Division')
    return fig

@app.callback(
    dash.dependencies.Output('stance-chart', 'figure'),
    [dash.dependencies.Input('div-dropdown', 'value')],
    [dash.dependencies.Input('radio-stance', 'value')],
)

def update_stance_chart(selected_division, selected_stance):
    lightweight_data = winner_division_results[selected_division]

    # Initialize lists to hold stances and total strikes landed
    stances = ['Orthodox', 'Southpaw', 'Switch']
    total_strikes_landed = []

    # Calculate the total strikes landed for each stance
    for stance in stances:
        total_strikes = lightweight_data[lightweight_data['stance'] == stance][selected_stance].sum()
        total_strikes_landed.append(total_strikes)

    #plot the grouped bar graph
    fig = px.bar(x=stances, y=total_strikes_landed, title=f' {selected_stance} by Stance in the {selected_division} Division', color=["Orthodox", "Southpaw", "Switch"], category_orders={"x": ["Orthodox", "Southpaw", "Switch"]}, labels={"x": "Stance", "y": f"{selected_stance}"})
    return fig

@app.callback(
    
    
    dash.dependencies.Output('correlation-graph', 'figure'),
    [dash.dependencies.Input('correlation-dropdown', 'value')],
    [dash.dependencies.Input('correlation-checklist', 'value')],
    [dash.dependencies.Input('correlation-checklist-yaxis', 'value')]

)

def update_correlation_graph(selected_division, selected_feature_x, selected_feature_y):
    # Filter the data for the selected division
    division_data = winner_division_results[selected_division]


    # Create the histplot
    df = winner_division_results[selected_division]
    fig = px.strip(df, x=selected_feature_x, y=selected_feature_y, title=f'{selected_feature_x} vs {selected_feature_y} in the {selected_division} Division'
)
    return fig
    
@app.callback(dash.dependencies.Output('fighter-full-stats-graph', 'figure'),
              [dash.dependencies.Input('fighter-stats-dropdown', 'value'), dash.dependencies.Input('fighter-specify-stats-dropdown', 'value')])
def update_fighter_stats_graph(fighter_name, fighter_stat_specification):
    # Filter the data for the selected fighter
    fighter_data = df.loc[df['fighter'] == fighter_name]
    #if result is chosen for fighter_stat_specification, tell the user that result==1 means the fighter won and result==0 means the fighter lost
  
    if fighter_stat_specification == 'result':
          fig = px.line(fighter_data, x='date', y=fighter_stat_specification, title=f'{fighter_stat_specification} for {fighter_name} (1 means the fighter won, 0 means the fighter lost)')
          return fig
    if fighter_stat_specification == 'control':
        fig = px.line(fighter_data, x='date', y=fighter_stat_specification, title=f'{fighter_stat_specification} (in seconds) for {fighter_name}')
        return fig
    if 'accuracy' in fighter_stat_specification:
        fig = px.line(fighter_data, x='date', y=fighter_stat_specification, title=f'{fighter_stat_specification} (in percentages) for {fighter_name}')
        return fig
    if 'differential' in fighter_stat_specification:
        fig = px.line(fighter_data, x='date', y=fighter_stat_specification, title=f'{fighter_stat_specification} for {fighter_name}')
        return fig
    # Create the line plot
    fig = px.line(fighter_data, x='date', y=fighter_stat_specification, title=f'{fighter_stat_specification} for {fighter_name}')
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
