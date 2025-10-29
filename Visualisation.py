# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import textwrap

# Loading the data generated from ESG topic modeling and scoring
df_topic = pd.read_csv(r"D:\VSCODE\ESG_Submission\Final_mapped_topics.csv")
df_score = pd.read_csv(r"D:\VSCODE\ESG_Submission\ESG_Topic_Modeling_Concreteness_Scores.csv")

# Data Preprocessing for visualization
df_score['filing_date'] = pd.to_datetime(df_score['filing_date']).dt.normalize()
df_topic['filing_date'] = pd.to_datetime(df_topic['filing_date']).dt.normalize()
df_topic['filing_year'] = df_topic['filing_date'].dt.year
# Select relevant columns
df_topic_selected = df_topic[['ticker', 'filing_date', 'Company Name', 'Sector',
                              'E_topic_name', 'S_topic_name', 'G_topic_name', 'ESG_topic_combination']]
# Merge datasets on ticker and filing_date
df_merged = df_score.merge(df_topic_selected, on=['ticker', 'filing_date'], how='inner')
df_merged['filing_year'] = df_merged['filing_date'].dt.year
df_merged['GRI'] = pd.to_numeric(df_merged['GRI'], errors='coerce').fillna(0)

# Function to get top topics per pillar per year
def get_top_topics(df):
    e_top = (df.groupby(['filing_year', 'E_topic_name']).size().reset_index(name='count')
             .sort_values(['filing_year', 'count'], ascending=[True, False])
             .groupby('filing_year').head(1)
             .assign(Pillar='E', Topic=lambda x: x['E_topic_name']))
    s_top = (df.groupby(['filing_year', 'S_topic_name']).size().reset_index(name='count')
             .sort_values(['filing_year', 'count'], ascending=[True, False])
             .groupby('filing_year').head(1)
             .assign(Pillar='S', Topic=lambda x: x['S_topic_name']))
    g_top = (df.groupby(['filing_year', 'G_topic_name']).size().reset_index(name='count')
             .sort_values(['filing_year', 'count'], ascending=[True, False])
             .groupby('filing_year').head(1)
             .assign(Pillar='G', Topic=lambda x: x['G_topic_name']))
    return pd.concat([e_top, s_top, g_top], ignore_index=True)[['filing_year', 'Pillar', 'Topic', 'count']]
# Precompute most dominant topics per year
top_topics_per_year = (df_topic.groupby(['filing_year', 'ESG_topic_combination'])
                       .size().reset_index(name='count')
                       .sort_values(['filing_year', 'count'], ascending=[True, False])
                       .groupby('filing_year', as_index=False).first())

# Create Dash app
app = dash.Dash(__name__)
app.title = "Decoding ESG: Measuring Clarity and Greenwashing in Corporate Disclosures"

# Layout of the dashboard
app.layout = html.Div([
    html.H2("Decoding ESG: Measuring Clarity and Greenwashing in Corporate Disclosures",
            style={'textAlign': 'center', 'color': 'white', 'marginBottom': '30px'}),

    # Filters on top of the dashboard
    html.Div([
        html.Div([
            html.Label("Select Sector(s):", style={'color': 'white'}),
            dcc.Dropdown(id='sector-filter', multi=True, placeholder="Select sectors")
        ], style={'width': '32%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select Company(s):", style={'color': 'white'}),
            dcc.Dropdown(id='company-filter', multi=True, placeholder="Select companies")
        ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'}),

        html.Div([
            html.Label("Select Year(s):", style={'color': 'white'}),
            dcc.Dropdown(id='year-filter', multi=True, placeholder="Select years")
        ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'})
    ], style={'marginBottom': '30px'}),

    # Top Row Charts
    html.Div([
        html.Div([dcc.Graph(id='overall-esg-line')], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='overall-gri-line')], style={'width': '49%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),

    # ESG Pillar Topics Chart
    html.Div([dcc.Graph(id='esg-pillar-year')],
             style={'width': '100%', 'marginBottom': '30px'}),

    # Title + Cards Row
    html.H4("Most Dominant Topics Across Years",
            style={'textAlign': 'center', 'color': 'white', 'marginBottom': '15px'}),

    html.Div([
        html.Div([dcc.Graph(id='card-e-topic')], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='card-s-topic')], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='card-g-topic')], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='card-esg-topic')], style={'width': '24%', 'display': 'inline-block'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '5px',
        'marginBottom': '30px'
    }),

    # Bottom Row
    html.Div([
        html.Div([dcc.Graph(id='dominant-topic-year')], style={'width': '65%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='esg-pie')], style={'width': '33%', 'display': 'inline-block', 'marginLeft': '2%'})
    ])
], style={'backgroundColor': '#111111', 'padding': '20px'})

# Callbacks for interactivity
@app.callback(
    Output('sector-filter', 'options'),
    Output('sector-filter', 'value'),
    Output('company-filter', 'options'),
    Output('company-filter', 'value'),
    Output('year-filter', 'options'),
    Output('year-filter', 'value'),
    Input('sector-filter', 'value')
)
# Update filter options and default selections based on selected sectors
def update_filters(selected_sectors):
    all_sectors = sorted(df_merged['Sector'].dropna().unique())
    default_sector = ["Information Technology"] if "Information Technology" in all_sectors else (all_sectors[:1] if all_sectors else [])
    sectors = selected_sectors if selected_sectors else default_sector
    filtered = df_merged[df_merged['Sector'].isin(sectors)]
    all_companies = sorted(filtered['ticker'].dropna().unique())
    all_years = sorted(filtered['filing_year'].dropna().unique())
    return (
        [{'label': s, 'value': s} for s in all_sectors],
        sectors,
        [{'label': c, 'value': c} for c in all_companies],
        all_companies[:3],
        [{'label': int(y), 'value': int(y)} for y in all_years],
        [int(y) for y in all_years]
    )

# Callback to update all charts based on filter selections
@app.callback(
    Output('overall-esg-line', 'figure'),
    Output('overall-gri-line', 'figure'),
    Output('esg-pillar-year', 'figure'),
    Output('dominant-topic-year', 'figure'),
    Output('card-e-topic', 'figure'),
    Output('card-s-topic', 'figure'),
    Output('card-g-topic', 'figure'),
    Output('card-esg-topic', 'figure'),
    Output('esg-pie', 'figure'),
    Input('sector-filter', 'value'),
    Input('company-filter', 'value'),
    Input('year-filter', 'value')
)
def update_charts(selected_sectors, selected_companies, selected_years):
    if not selected_sectors:
        selected_sectors = df_merged['Sector'].dropna().unique().tolist()
    if not selected_companies:
        selected_companies = df_merged['ticker'].dropna().unique().tolist()
    if not selected_years:
        selected_years = df_merged['filing_year'].dropna().unique().tolist()
    selected_years = [int(y) for y in selected_years]

    df_filtered = df_merged[
        (df_merged['Sector'].isin(selected_sectors)) &
        (df_merged['ticker'].isin(selected_companies)) &
        (df_merged['filing_year'].isin(selected_years))
    ]

    if df_filtered.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(template='plotly_dark', title='No data available for selected filters')
        return [empty_fig] * 9

    # Overall ESG Line (with overall average line which scales with companies selected)
    overall_esg = df_filtered.groupby(['filing_year', 'Company Name'])['Overall_ESG_content'].mean().reset_index()
    overall_avg_esg = df_merged.groupby('filing_year')['Overall_ESG_content'].mean().reset_index()
    overall_avg_esg['Company Name'] = 'Overall Average'
    combined_esg = pd.concat([overall_esg, overall_avg_esg])
    # Create line chart for Overall ESG Content
    fig_esg = px.line(
        combined_esg,
        x='filing_year', y='Overall_ESG_content',
        color='Company Name',
        markers=True,
        title='Overall ESG Content Over Years',
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Plotly + ['#FFD700']
    )
    fig_esg.for_each_trace(lambda t: t.update(line=dict(width=3, dash='dot')) if t.name == 'Overall Average' else ())
    fig_esg.update_layout(title_x=0.5)

    # Overall GRI Line (with overall average line which scales with companies selected)
    overall_gri = df_filtered.groupby(['filing_year', 'Company Name'])['GRI'].mean().reset_index()
    overall_avg_gri = df_merged.groupby('filing_year')['GRI'].mean().reset_index()
    overall_avg_gri['Company Name'] = 'Overall Average'
    combined_gri = pd.concat([overall_gri, overall_avg_gri])
    # Create line chart for GRI
    fig_gri = px.line(
        combined_gri,
        x='filing_year', y='GRI',
        color='Company Name',
        markers=True,
        title='GRI Scores Over Years',
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Plotly + ['#FFD700']
    )
    fig_gri.for_each_trace(lambda t: t.update(line=dict(width=3, dash='dot')) if t.name == 'Overall Average' else ())
    fig_gri.update_layout(title_x=0.5)

    # ESG Pillar Topics per Year Bar Chart
    top_per_pillar = get_top_topics(df_filtered)
    fig_pillar = px.bar(
        top_per_pillar,
        x='filing_year', y='count', color='Pillar', text='Topic',
        barmode='group',
        title='Most Discussed E, S, and G Topics per Year',
        labels={'filing_year': 'Filing Year', 'count': 'Number of Filings'},
        color_discrete_map={'E': '#2ca02c', 'S': '#1f77b4', 'G': '#ff7f0e'},
        template='plotly_dark'
    )
    fig_pillar.update_traces(
        textposition='outside',
        hovertemplate="<b>Year:</b> %{x}<br><b>Topic:</b> %{text}<br><b>Count:</b> %{y}<extra></extra>"
    )
    fig_pillar.update_layout(
        xaxis=dict(tickmode='linear', title='Filing Year'),
        yaxis_title='Number of Filings',
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font=dict(color='white'),
        showlegend=True,
        legend_title_text='ESG Pillar',
        bargap=0.3,
        title_x=0.5
    )

    # Dominant Topic per Year Bar Chart
    filtered_top_topics_year = top_topics_per_year[top_topics_per_year['filing_year'].isin(selected_years)]
    fig_dom_year = px.bar(
        filtered_top_topics_year,
        x='filing_year', y='count',
        color='ESG_topic_combination',
        title='Most Dominant ESG Topic per Year',
        template='plotly_dark'
    )
    fig_dom_year.update_traces(
        hovertemplate="<b>Year:</b> %{x}<br><b>Topic:</b> %{customdata[0]}<extra></extra>",
        customdata=filtered_top_topics_year[['ESG_topic_combination']]
    )
    fig_dom_year.update_layout(showlegend=False, title_x=0.5)

    # Cards for Most Dominant Topics
    def make_card(title, topic, color):
        fig = go.Figure()
        wrapped = "<br>".join(textwrap.wrap(topic, width=25))
        fig.add_annotation(
            text=f"<b>{title}</b><br>{wrapped}",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color='white'),
            align='center',
            bordercolor=color, borderwidth=2, borderpad=8,
            bgcolor='#1c1c1c'
        )
        fig.update_layout(
            template='plotly_dark',
            height=200,
            margin=dict(l=2, r=2, t=5, b=5),
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    # Determine most dominant topics overall
    e_dom = df_filtered['E_topic_name'].value_counts().idxmax() if not df_filtered.empty else "N/A"
    s_dom = df_filtered['S_topic_name'].value_counts().idxmax() if not df_filtered.empty else "N/A"
    g_dom = df_filtered['G_topic_name'].value_counts().idxmax() if not df_filtered.empty else "N/A"
    overall_dom = df_filtered['ESG_topic_combination'].value_counts().idxmax() if not df_filtered.empty else "N/A"
    # Creating cards for each dominant topic
    card_e = make_card("Most Dominant Environmental Theme", e_dom, "#2ca02c")
    card_s = make_card("Most Dominant Social Theme", s_dom, "#1f77b4")
    card_g = make_card("Most Dominant Governance Theme", g_dom, "#ff7f0e")
    card_esg = make_card("Most Dominant ESG Theme", overall_dom, "#9467bd")

    # ESG Composition Pie Chart (Average across selected data)
    esg_avg = pd.DataFrame({
        'Pillar': ['E', 'S', 'G'],
        'Percentage': [
            df_filtered['E_percentage_in_report'].mean(),
            df_filtered['S_percentage_in_report'].mean(),
            df_filtered['G_percentage_in_report'].mean()
        ]
    })
    pie = px.pie(
        esg_avg, names='Pillar', values='Percentage',
        title='Average ESG Composition (Selected Years)',
        hole=0.45,
        color_discrete_map={'E': '#2ca02c', 'S': '#1f77b4', 'G': '#ff7f0e'},
        template='plotly_dark'
    )
    pie.update_layout(title_x=0.5)

    return fig_esg, fig_gri, fig_pillar, fig_dom_year, card_e, card_s, card_g, card_esg, pie


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
