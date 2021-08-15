import numpy as np
import pandas as pd

#import plotly renderer for viewing web interactive charts
import plotly.io as pio
#pio.renderers.default = 'iframe' # or 'notebook' or 'colab'


import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

import dash_bootstrap_components as dbc

# %%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = '''
The U.S. Census reports that women won't achieve equal pay to men until 2059 (if 2020 trends continue). There is not one single predictor of this effect. The  gender pay/wage gap exists within industries, and across wage and education levels.   

The General Social Survey (GSS) is a nationally respresentive survey of U.S. adults and asks repondants about various demographic, behaviorial, and attiudional questions. 

This dashboard uses responses from the GSS to explore the wage gap. 

Sources: https://www.census.gov/library/stories/2020/03/equal-pay-day-is-march-31-earliest-since-1996 & http://www.gss.norc.org/About-The-GSS
'''

myvar = ["income", "job_prestige", "socioeconomic_index", "education", "sex"]

mydf = gss_clean[myvar]

# mydf

# display = mydf.groupby('sex').agg({'income':'mean',
#                                     'job_prestige':'mean',
#                                    'socioeconomic_index' : "mean" , 
#                                    'education' : 'mean'
#                                   }).reset_index()
# display = round(display, 2)
# display

# p2 = ff.create_table(display)
# p2.show()

# bread_plot = gss_clean.groupby(['sex', 'male_breadwinner']).size()
# bread_plot = bread_plot.reset_index()
# bread_plot = bread_plot.rename({0:'count'}, axis=1)
# bread_plot

# p3 = px.bar(bread_plot, x = 'male_breadwinner', y = 'count', color = 'sex', barmode = 'group', 
#             color_discrete_map = {'male':'blue', 'female':'red'}, 
#             category_orders = {"male_breadwinner" : ["strongly disagree" , "disagree", "agree", "strongly agree"]})

# p3.show()


# p4 = px.scatter(gss_clean, x='job_prestige', y='income', color = 'sex',
#                  height=600, width=600,
#                  trendline = 'ols',
#                  labels={'income':'income', 
#                         'job_prestige':'job prestige'},
#                  hover_data=['education', 'socioeconomic_index'])
# p4.update(layout=dict(title=dict(x=0.5)))
# p4.show()

# p5a = px.box(gss_clean, y='income', color = 'sex',
#              color_discrete_map = {'male':'blue', 'female':'red'}, 
#                    labels={'income':'income'})
# p5a.update_layout(showlegend=False)
# p5a.show()

# p5b = px.box(gss_clean, y='job_prestige', color = 'sex',
#               color_discrete_map = {'male':'blue', 'female':'red'}, 
#                    labels={'job_prestige':'job prestige'})
# p5b.update_layout(showlegend=False)
# p5b.show()

mycol = ['income', 'sex', 'job_prestige']
mydf = gss_clean[mycol]

# mydf

mydf['job_cat'] = pd.cut(mydf.job_prestige, bins = 6, labels = ('level 1', 'level 2', 'level 3', 'level 4', 'level 5', 'level 6'))

# mydf.head()

# mydf.shape


mydf = mydf.dropna()
# mydf.shape

p6 = px.box(mydf, y='income', color = 'sex', 
              facet_col = 'job_cat', facet_col_wrap=2,
                   labels={'income':'income', 'job_cat' : "job prestige"}, 
              color_discrete_map = {'male':'blue', 'female':'red'}, 
              category_orders = {"job_cat" : ['level 1', 'level 2', 'level 3', 'level 4', 'level 5', 'level 6']})
p6.update_layout(showlegend=False)
p6.show()



#start dashboard
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.layout = html.Div(
    [
        html.H1("Exploring the wage gap in the GSS"), #list contains individual elements of dashboard
        dcc.Markdown(children = markdown_text),
        
        #html.H2("Mean income, occupational prestige, socioeconomic index, and years of education: by sex"),
        #dcc.Graph(figure = p2),
        
        #html.H2("Agreement with 'men should be the breadwinner': by sex"),
        #dcc.Graph(figure = p3),
        
        #html.H2("Job prestige vs. income: by sex"),
        #dcc.Graph(figure = p4),
        
        #html.H2("Income distribution: by sex"),
        #dcc.Graph(figure = p5a),
        
        #html.H2("Job prestige distribution: by sex"),
        #dcc.Graph(figure = p5b),
        
        html.H2("Job prestige (catagorical) v. income: by sex"),
        dcc.Graph(figure = p6),
        
        
        
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)


