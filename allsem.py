import altair as alt
import pandas as pd
import datapane as dp
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

# Sign-in with your unique token
dp.login(token="a7f3b829ac6a2e8d3c1d15c0f5544f88e1031acf")

df_au19 = pd.read_csv('data/au19.csv')
df_sp20 = pd.read_csv('data/au19.csv')
df_au20 = pd.read_csv('data/au19.csv')

num_students = len(df_au19) + len(df_sp20) + len(df_au20)

html = """
<html>
    <style type='text/css'>
        @keyframes example {
            0%   {color: #EEE;}
            25%  {color: #EC4899;}
            50%  {color: #8B5CF6;}
            100% {color: #EF4444;}
        }
        #container {
            background: #1F2937;
            padding: 10em;
        }
        h1 {
            color:#eee;
            animation-name: example;
            animation-duration: 4s;
            animation-iteration-count: infinite;
        }
    </style>
    <div id="container">
      <h1 style="text-indent: 150px"> CSE 1223 Over the Semesters Dashboard </h1>
    </div>
</html>
"""

final_avg_au19 = round(df_au19["Final Grade"].mean(), 2)
final_avg_sp20 = round(df_sp20["Final Grade"].mean(), 2)
final_avg_au20 = round(df_au20["Final Grade"].mean(), 2)

sem_labels = ['AU19', 'SP20', 'AU20']
final_grades = [final_avg_au19, final_avg_sp20, final_avg_au20]

final_bar = go.Figure(go.Bar(name='Final Grades over 3 Semesters', x=sem_labels, y=final_grades))
final_bar.update_traces(marker_color='rgb(147,112,219)', marker_line_color='rgb(148,0,211)', marker_line_width=1.5, opacity=0.6)
final_bar.update_layout(xaxis_title='semester', yaxis_title='average')
final_bar.update_yaxes(range=[0,100])

# Create report
r = dp.Report(
    dp.Page(
        label='Introduction',
        blocks=[
            dp.HTML(html),
            "The data has been compiled over 3 semesters, for the introductory computer science class CSE 1223.",
            dp.BigNumber(heading="Number of Students", value=num_students)
        ]
    ),
    dp.Page(
        label='Final Grades',
        blocks=[
            f'### Overall',
            dp.Plot(final_bar)
        ]
    )
)

# Publish
r.publish(name=f'CSE 1223 Multi-Semester Dashboard', open=True, description=f'Grade Data for CSE 1223 over multiple semesters')
