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

dataset = pd.read_csv('data/au19.csv')

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
      <h1 style="text-indent: 300px"> CSE 1223 Dashboard </h1>
    </div>
</html>
"""

fig = px.histogram(dataset, x="Final Grade")

# def f(col):
#     fig = px.histogram(dataset, x=col)
#     # dataset.loc[col].iplot(
#     #     xTitle='Student', 
#     #     yTitle='Grades for {}'.format(col),
#     #     title='Grades for Students'
#     #     )

# interact(f, col=list(dataset.columns))

# fig = f(dataset.columns)

fig = px.histogram(dataset, x="Final Grade")

exam_labels = ['midterm1', 'midterm2', "final"]
fig2 = ff.create_distplot([dataset['Midterm I (43527)'], dataset['Midterm II (43528)'], dataset['Final Exam (43512)']], exam_labels)

class_average = round(dataset["Final Grade"].mean(), 2)
num_students = len(dataset)
pass_rate = round( (np.sum(dataset['Final Grade'] >= 60)) * 100 / num_students, 2)

female = dataset[dataset['SEX'] == 'F']['Final Grade']
male = dataset[dataset['SEX'] == 'M']['Final Grade']

sex_labels = ['Female', 'Male']
sex_comp = ff.create_distplot([female, male], sex_labels)

# bar_df = df = pd.DataFrame(columns=["MT1", "MT2"], data=[[5,np.nan]])

# fig = px.bar(bar_df, x="sex", y="total_bill",
#              color='SEX', barmode='group',
#              height=400)

 
#animals=['MT1', 'MT2', 'Final']

female = dataset.loc[dataset['SEX'] == 'F']
male = dataset.loc[dataset['SEX'] == 'M']

bar_fig = go.Figure(data=[
    go.Bar(name='Female', x=exam_labels, y=[female['Midterm I (43527)'].mean(), female['Midterm II (43528)'].mean(), female['Final Exam (43512)'].mean()]),
    go.Bar(name='Male', x=exam_labels, y=[male['Midterm I (43527)'].mean(), male['Midterm II (43528)'].mean(), male['Final Exam (43512)'].mean()])
])
# Change the bar mode
bar_fig.update_layout(xaxis_title='assignment', yaxis_title='average', legend_title='sex', barmode='group')


# Create report
r = dp.Report(
    dp.Page(
        label='Introduction',
        blocks=[
            dp.HTML(html),
            "The data has been compiled over 3 semesters, for the introductory computer science class CSE 1223.",
            dp.Group(
                dp.BigNumber(heading="Number of Students", value=num_students),
                dp.BigNumber(
                    heading="Class Average", 
                    value=str(class_average) + "%",
                    change="2%",
                    is_upward_change=True),
                columns=2
            ),
            dp.BigNumber(heading="Pass Rate", value=str(pass_rate) + "%"),
        ]
    ),
    dp.Page(
        label='Final Grades',
        blocks=[
        f'### Comparing Final Grade Data ',
        dp.Plot(fig)]
    ),
    dp.Page(
        label='Exam Grades',
        blocks=[
        f'### Kernel Density Plot ',
        dp.Plot(fig2)]
    ),
    dp.Page(
        dp.Select(blocks=[
            dp.Plot(sex_comp, label='Hist'),
            dp.Plot(bar_fig, label='Bar Chart')
        ], type=dp.SelectType.DROPDOWN),
        label='Demographics'
        #blocks=[f'### Comparing Final Grade Data among Various Demographics']
    )
    #dp.DataTable(df),
)

# Publish
r.publish(name=f'CSE 1223 Dashboard', open=True, description=f'Grade Data for CSE 1223')

