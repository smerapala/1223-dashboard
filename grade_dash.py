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

# INTRODUCTION TAB
class_average = round(dataset["Final Grade"].mean(), 2)
num_students = len(dataset)
pass_rate = round( (np.sum(dataset['Final Grade'] >= 60)) * 100 / num_students, 2)


# DELIVERABLES TAB


# EXAM GRADES TAB
exam_labels = ['midterm1', 'midterm2', "final"]
exams_kdp = ff.create_distplot([dataset['Midterm I (43527)'], dataset['Midterm II (43528)'], dataset['Final Exam (43512)']], exam_labels)


# FINAL GRADES TAB
fg_hist = px.histogram(dataset, x="Final Grade")

letter_pie = go.Figure(go.Pie(labels= dataset["CRSE_GRADE_OFF"]))


# DEMOGRAPHICS TAB
lab_labels = ['Fill An Array', 'Introducing Methods', 'Using The Debugger', 'Fill An Array Randomly', 'Fun With Files',
    'ROT13 Encryption', 'Fun With Lists', 'Fun With Classes']

hw_labels = ['Participation', 'Reading Assignment 2', 'Reading Assignment 3', 'Reading Assignment 4', 'Reading Assignment 5',
    'Tracing Table Practice', 'Reading Assignment 6','Reading Assignment 7','Reading Assignment 8', 'Reading Assignment 9',
    'Reading Assignment 10', 'Background Survey']

lab_grades = []
for label in lab_labels:
    lab_grades.append( dataset[label].mean() * 100 / dataset[label].max() )

lab_bar = go.Figure(go.Bar(name='Lab Grades', x=lab_labels, y=lab_grades))
lab_bar.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
lab_bar.update_layout(xaxis_title='lab assignment', yaxis_title='average' )


# Sex - Histogram
female_cols = dataset[dataset['SEX'] == 'F']['Final Grade']
male_cols = dataset[dataset['SEX'] == 'M']['Final Grade']
sex_labels = ['Female', 'Male']
sex_kdp = ff.create_distplot([female_cols, male_cols], sex_labels)

# Sex - Bar Chart
female_df = dataset.loc[dataset['SEX'] == 'F']
male_df = dataset.loc[dataset['SEX'] == 'M']

sex_bar = go.Figure(data=[
    go.Bar(name='Female', x=exam_labels, y=[female_df['Midterm I (43527)'].mean(), female_df['Midterm II (43528)'].mean(), female_df['Final Exam (43512)'].mean()]),
    go.Bar(name='Male', x=exam_labels, y=[male_df['Midterm I (43527)'].mean(), male_df['Midterm II (43528)'].mean(), male_df['Final Exam (43512)'].mean()])
])
# Change the bar mode
sex_bar.update_layout(xaxis_title='assignment', yaxis_title='average', legend_title='sex', legend_bordercolor='black', legend_borderwidth=2, barmode='group', bargap=.6)

# URM - Bar Chart
urm_df = dataset.loc[dataset['URM Status'] == 'URM']
nonurm_df = dataset.loc[dataset['URM Status'] == 'Non-URM']

urm_bar = go.Figure(data=[
    go.Bar(name='URM', x=exam_labels, y=[urm_df['Midterm I (43527)'].mean(), urm_df['Midterm II (43528)'].mean(), urm_df['Final Exam (43512)'].mean()]),
    go.Bar(name='Non-URM', x=exam_labels, y=[nonurm_df['Midterm I (43527)'].mean(), nonurm_df['Midterm II (43528)'].mean(), nonurm_df['Final Exam (43512)'].mean()])
])
# Change the bar mode
urm_bar.update_layout(xaxis_title='assignment', yaxis_title='average', legend_title='URM Status', legend_bordercolor='black', legend_borderwidth=2, barmode='group', bargap=.6)

# Race - Bar Chart
white_df = dataset.loc[dataset['OCC_RPT_ETH_CD_DSC'] == 'White']
asian_df = dataset.loc[dataset['OCC_RPT_ETH_CD_DSC'] == 'Asian']
black_df = dataset.loc[dataset['OCC_RPT_ETH_CD_DSC'] == 'Black or African American']
hispanic_df = dataset.loc[dataset['OCC_RPT_ETH_CD_DSC'] == 'Hispanic']
alien_df = dataset.loc[dataset['OCC_RPT_ETH_CD_DSC'] == 'Non-Resident Alien']

race_bar = go.Figure(data=[
    go.Bar(name='White', x=exam_labels, y=[white_df['Midterm I (43527)'].mean(), white_df['Midterm II (43528)'].mean(), white_df['Final Exam (43512)'].mean()]),
    go.Bar(name='Asian', x=exam_labels, y=[asian_df['Midterm I (43527)'].mean(), asian_df['Midterm II (43528)'].mean(), asian_df['Final Exam (43512)'].mean()]),
    go.Bar(name='Black/African American', x=exam_labels, y=[black_df['Midterm I (43527)'].mean(), black_df['Midterm II (43528)'].mean(), black_df['Final Exam (43512)'].mean()]),
    go.Bar(name='Hispanic', x=exam_labels, y=[hispanic_df['Midterm I (43527)'].mean(), hispanic_df['Midterm II (43528)'].mean(), hispanic_df['Final Exam (43512)'].mean()]),
    go.Bar(name='Non-resident Alien', x=exam_labels, y=[alien_df['Midterm I (43527)'].mean(), alien_df['Midterm II (43528)'].mean(), alien_df['Final Exam (43512)'].mean()])
])
# Change the bar mode
race_bar.update_layout(xaxis_title='assignment', yaxis_title='average', legend_title='Race', legend_bordercolor='black', legend_borderwidth=2, barmode='group', bargap=.3)


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
        label='Deliverables',
        blocks=[
        f'### Labs',
        dp.Plot(lab_bar),
        # f'### Homeworks',
        # dp.Plot(hw_bar),
        #  f'### Projects',
        # dp.Plot(project_bar)
        ]
    ),
    dp.Page(
        label='Exam Grades',
        blocks=[
        f'### Kernel Density Plot ',
        dp.Plot(exams_kdp)]
    ),
    dp.Page(
        label='Final Grades',
        blocks=[
        f'### Comparing Final Grade Data ',
        dp.Plot(fg_hist),
        dp.Plot(letter_pie)
        ]
    ),
    dp.Page(
        dp.Select(blocks=[
            dp.Plot(sex_bar, label='Sex-Bar Chart'),
            dp.Plot(urm_bar, label='URM-Bar Chart'),
            dp.Plot(race_bar, label='Race-Bar Chart'),
            dp.Plot(sex_kdp, label='Sex-KDP')
        ], type=dp.SelectType.DROPDOWN),
        label='Demographics',
        #blocks=[f'### Comparing Final Grade Data among Various Demographics']
    )
)

# Publish
r.publish(name=f'CSE 1223 Dashboard AU19', open=True, description=f'Grade Data for CSE 1223 during the AU19 semester')
