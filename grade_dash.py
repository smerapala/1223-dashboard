import altair as alt
import pandas as pd
import datapane as dp
#import scipy
import plotly.express as px
import plotly.figure_factory as ff
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

# Sign-in with your unique token
dp.login(token="a7f3b829ac6a2e8d3c1d15c0f5544f88e1031acf")

dataset = pd.read_csv('data/grades.csv')
# locations = dataset[['location', 'ID']].sample(3) # Replace with you own locations to customize!

# df = dataset[dataset.iso_code.isin(locations.iso_code)]

# plot = alt.Chart(df).mark_area(opacity=0.4, stroke='black').encode(
#     x='date:T', y=alt.Y('new_cases_smoothed_per_million:Q', stack=None),
#     color=alt.Color('location:N', scale=alt.Scale(scheme='set1')), tooltip='location:N'
# ).interactive().properties(width='container')

def f(col):
    dataset.loc[col].iplot(
        xTitle='Student', 
        yTitle='Grades for {}'.format(col),
        title='Grades for Students'
        )

interact(f, col=dataset.index)

fig = px.histogram(dataset, x="Final Grade")
fig.show()

group_labels = ['midterm1', 'midterm2']
fig2 = ff.create_distplot([dataset['Midterm I (43527)'], dataset['Midterm II (43528)']], group_labels)

# Create report
r = dp.Report(
    f'### Comparing Final Grade Data ',
    dp.Plot(fig),
    dp.Markdown("Kernel Density Plot"),
    dp.Plot(fig2)
    #dp.DataTable(df),
)

# Publish
r.publish(name=f'Final Grade Data', open=True, description=f'Final Grade Data for CSE 1223')

