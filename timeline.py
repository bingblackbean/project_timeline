import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import pandas as pd

df = pd.DataFrame(
    [
        dict(
            Task="Job-1",
            Start='2017-01-01',
            Finish='2017-02-02',
            Resource='Complete'),
        dict(
            Task="Job-1",
            Start='2017-02-15',
            Finish='2017-03-15',
            Resource='Incomplete'),
        dict(
            Task="Job-2",
            Start='2017-01-17',
            Finish='2017-02-17',
            Resource='Not Started'),
        dict(
            Task="Job-2",
            Start='2017-01-17',
            Finish='2017-02-17',
            Resource='Complete'),
        dict(
            Task="Job-3",
            Start='2017-03-10',
            Finish='2017-03-20',
            Resource='Not Started'),
        dict(
            Task="Job-3",
            Start='2017-04-01',
            Finish='2017-04-20',
            Resource='Not Started'),
        dict(
            Task="Job-3",
            Start='2017-05-18',
            Finish='2017-06-18',
            Resource='Not Started'),
        dict(
            Task="Job-4",
            Start='2017-01-14',
            Finish='2017-03-14',
            Resource='Complete')])


colors = {'Not Started': 'rgb(15, 0, 0)',
          'Incomplete': 'rgb(220, 0, 0)',
          'Complete': 'rgb(0, 255, 100)'}


app = dash.Dash(__name__)


app.layout = html.Div([dcc.Graph(id='adding-rows-graph'),
                       dash_table.DataTable(
    id='adding-rows-table',
    columns=[{
        'name': i,
        'id': i,
        'deletable': True,
        'renamable': False
    } for i in df.columns],
    data=df.to_dict('records'),
    editable=True,
    row_deletable=True,
    page_action='native',
    page_current=0,
    page_size=5
),
    html.Button('Add Row', id='editing-rows-button', n_clicks=0)
])


@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output('adding-rows-graph', 'figure'),
    Input('adding-rows-table', 'data'))
def display_output(data):
    fig = ff.create_gantt(
        data,
        colors=colors,
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        title='Project Timeline')
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
