import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import requests
from pymongo import MongoClient
from bson import json_util



#data=pd.read_excel('curva.xlsx')






#from bs4 import BeautifulSoup
#import pandas as pd
#from datetime import date, datetime, timedelta
#import json

#import plotly.express as px
#import plotly.graph_objects as go
#import streamlit as st
#import pandas as pd



user= 'pardeep'
password = 'khalsakhalsa'
db = 'myFirstDatabase'
db_name = 'Scrapped_'



def connet_mongo(user,password,db,db_name):
    mongo_url =  'mongodb+srv://{}:{}@cluster0.o88ol.mongodb.net/{}?retryWrites=true&w=majority'.format(user,password,db)
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db.CFPB_.find_one()
    return collection

mongo_data = connet_mongo(user,password,db,db_name)


df1 = pd.DataFrame(mongo_data.get('hits').get('hits')[0].get('_source'),index=[0])

for i in range(len(mongo_data.get('hits').get('hits'))-1):
    df2 = pd.DataFrame(mongo_data.get('hits').get('hits')[i+1].get('_source'),index=[0])
    df1 = pd.concat([df1,df2])

weekday = df1.groupby([pd.DatetimeIndex(df1['date_received']).weekday]).agg({'count'})['date_received']




df1['company_response'].replace({'Closed with non-monetary relief':'Closed with explanation','Untimely response':'In progress'},inplace=True)

df1['consumer_consent_provided'].replace({'None':'N/A','Other':'N/A'},inplace=True)

df1['tags'].replace({'Older American, Servicemember':'Older American'},inplace=True)










html_header="""
<head>
<title>PControlDB</title>
<meta charset="utf-8">
<meta name="keywords" content="projectl control, dashboard, management, EVA">
<meta name="description" content="project control dashboard">
<meta name="author" content="Larry Prato">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<h1 style="font-size:300%; color:#008080; text-align: center; font-family:Georgia"; > Consumer Financial Protection Bureau <br>
 <h6 style="color:#008080;  font-family:Georgia"> - The Consumer Financial Protection Bureau is a U.S. government agency that makes sure banks, lenders, and other financial companies treat you fairly.
 </h6	> <br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""
st.set_page_config(page_title="CFPB", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


html_card_header1="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 350px;
   height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Total Complaints</h3> <!--  1st Component Heading -->  
  </div>
</div>
"""


html_card_footer1="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 350px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">As per CFPB USA Data # OF COMPLAINTS ARE REGISTERED</p>
  </div>
</div>
"""

html_card_header2="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 350px;
   height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Below TAT</h3> <!-- 2nd component heading  -->
  </div>
</div>
"""
html_card_footer2="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 350px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;"># of Complaints Sucessfully resolved in given time frame</p>
  </div>
</div>
"""
html_card_header3="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 350px;
   height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Above TAT</h3> <!-- 3rd Component Heading -->
  </div>
</div>
"""
html_card_footer3="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 350px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;"># of Complaints Failed to Resolved in given Time Frame</p>
  </div>
</div>
"""




#option2 = st.sidebar.selectbox('Which Tags you want to filter?',tuple(df1['company'].unique()))

#st.write(option2)

#df1 = df1[df1['tags']==option2]	



option1 = st.sidebar.selectbox('Which Product you would like to Select?',tuple(df1['product'].unique()),1)

df1 = df1[df1['product']==option1]







# 1st block
TOTAL_COMPLAINTS = df1['complaint_id'].count()
TIMELY_COMPLETED =  df1[df1['timely']=='Yes']['complaint_id'].count()
TIMELY_INCOMPLETED =  df1[df1['timely']=='No']['complaint_id'].count()



with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,15,1,15,1,15,1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header1, unsafe_allow_html=True)
        fig_c1 = go.Figure(go.Indicator(
            mode="number+delta",
            value=TOTAL_COMPLAINTS, # here we use the 1st component value 
            number={'suffix': "", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
            #delta={'position': "bottom", 'reference': 60, 'relative': False}, # HERE WE USE 1ST  COMPONENT INDICATOR
            domain={'x': [0, 1], 'y': [0, 1]}))
        fig_c1.update_layout(autosize=False,
                             width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                             paper_bgcolor="#fbfff0", font={'size': 20})
        st.plotly_chart(fig_c1)
        st.markdown(html_card_footer1, unsafe_allow_html=True)
    with col3:
        st.write("")
    with col4:
        st.markdown(html_card_header2, unsafe_allow_html=True)
        fig_c2 = go.Figure(go.Indicator(
            mode="number+delta",
            value=TIMELY_COMPLETED, #here we use the 2nd component value 
            number={'suffix': "", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}, 'valueformat': ',f'},
            #delta={'position': "bottom", 'reference': 732}, # HERE WE USE 2ND  COMPONENT INDICATOR
            domain={'x': [0, 1], 'y': [0, 1]}))
        fig_c2.update_layout(autosize=False,
                             width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                             paper_bgcolor="#fbfff0", font={'size': 20})
        fig_c2.update_traces(delta_decreasing_color="#3D9970",
                             delta_increasing_color="#FF4136",
                             delta_valueformat='f',
                             selector=dict(type='indicator'))
        st.plotly_chart(fig_c2)
        st.markdown(html_card_footer2, unsafe_allow_html=True)
    with col5:
        st.write("")
    with col6:
        st.markdown(html_card_header3, unsafe_allow_html=True)
        fig_c3 = go.Figure(go.Indicator(
            mode="number+delta",
            value=TIMELY_INCOMPLETED,  #here we use the 3rd component value 
            number={"font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
            #delta={'position': "bottom", 'reference': 1.09, 'relative': False}, # HERE WE USE 3RD  COMPONENT INDICATOR
            domain={'x': [0, 1], 'y': [0, 1]}))
        fig_c3.update_layout(autosize=False,
                             width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                             paper_bgcolor="#fbfff0", font={'size': 20})
        fig_c3.update_traces(delta_decreasing_color="#3D9970",
                             delta_increasing_color="#FF4136",
                             delta_valueformat='.3f',
                             selector=dict(type='indicator'))
        st.plotly_chart(fig_c3)
        st.markdown(html_card_footer3, unsafe_allow_html=True)
    with col7:
        st.write("")
html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)


html_card_header4="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 300px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 10px 0;">Consent Wise CMP</h4>  <!-- 4th Component Heading -->
  </div>
</div>
"""
html_card_footer4="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Montly Value (%)</p>
  </div>
</div>
"""
html_card_header5="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px;  margin-left: 20px;  width: 250px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 10px 0;">CMP Response</h4> <!-- 5th Component Heading -->
  </div>
</div>
"""
html_card_footer5="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Montly Relative Change (%)</p>
  </div>
</div>
"""



### Block 2#########################################################################################
with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,10,1,20,1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header4, unsafe_allow_html=True)
        x = df1['consumer_consent_provided'].value_counts().index # 4th component legend
        y = df1['consumer_consent_provided'].value_counts().values # 4th component value	
        fig_m_prog = go.Figure([go.Bar(x=x, y=y, text=y, textposition='auto')])
        fig_m_prog.update_layout(paper_bgcolor="#fbfff0", plot_bgcolor="#fbfff0",
                                 font={'color': "#008080", 'family': "Arial"}, height=200, width=300,
                                 margin=dict(l=30, r=10, b=4, t=10))
        fig_m_prog.update_yaxes(title='y', visible=False, showticklabels=False)
        fig_m_prog.update_traces(marker_color='#17A2B8', selector=dict(type='bar'))
        st.plotly_chart(fig_m_prog)
        st.markdown(html_card_footer4, unsafe_allow_html=True)
    with col3:
        st.write("")
        st.write("")		
    with col4:
        st.markdown(html_card_header5, unsafe_allow_html=True)
        x = df1['company_response'].value_counts().index # 5th Component legend
        y = df1['company_response'].value_counts().values #5th Component Value
        fig_m_hh = go.Figure([go.Bar(x=x, y=y, text=y, textposition='auto')])
        fig_m_hh.update_layout(paper_bgcolor="#fbfff0", plot_bgcolor="#fbfff0",
                               font={'color': "#008080", 'family': "Arial"}, height=200, width=300,
                               margin=dict(l=20, r=1, b=100, t=1))
        fig_m_hh.update_yaxes(title='y', visible=False, showticklabels=False)
        fig_m_hh.update_traces(marker_color='#17A2B8', selector=dict(type='bar'))
        st.plotly_chart(fig_m_hh)
        st.markdown(html_card_footer5, unsafe_allow_html=True)
    with col5:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
#    with col6:
#        st.write("")		
    with col6:
        #y = data.loc[data.Activity_name == 'Total']
        # Create traces
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=weekday.index, y=weekday['count'],
                                  mode='lines',
                                  name='Complaints',
                                  marker_color='#17A2B8'))
        #fig3.add_trace(go.Scatter(x=weekday.index, y=weekday['count'],
        #                                marker_color='#17A2B8'))
        fig3.update_layout(title={'text': "Week Wise Complaints", 'x': 1}, paper_bgcolor="#fbfff0", #6th Component heading
                           plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 12, 'family': "Georgia"}, height=220,
                           width=500,
                           legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01),
                           margin=dict(l=1, r=1, b=1, t=30))
        #fig3.update_xaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=6, rangemode="tozero",
        #                  showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7')
        #fig3.update_yaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=10, rangemode="tozero",
         #                 showgrid=True, gridwidth=0.5, gridcolor='#F7F7F7')
        fig3.layout.yaxis.tickformat = ',.0'
        st.plotly_chart(fig3)
    with col7:
        st.write("")

html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)

html_card_header6="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 10px 0;">Closed %</h4>
  </div>
</div>
"""
html_card_footer6="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Montly Value </p>
  </div>
</div>
"""
html_card_header7="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 10px 0;">InProgrss %</h4>
  </div>
</div>
"""
html_card_footer7="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Montly Value</p>
  </div>
</div>
"""







closed_cmp_perc =  int((df1[df1['company_response' ]== 'Closed with explanation']['complaint_id'].count()/TOTAL_COMPLAINTS)*100)
Inprogrss_cmp_perc =  int((df1[df1['company_response' ]== 'In progress']['complaint_id'].count()/TOTAL_COMPLAINTS)*100)

### Block 3#########################################################################################
with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,10,1,20,1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header6, unsafe_allow_html=True)
        fig_cv = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=closed_cmp_perc,   #7th Component Value 
            number={'suffix': "%", "font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': "#06282d"},
                'bgcolor': "white",
                'steps': [
                    {'range': [0, closed_cmp_perc], 'color': '#FF4136'},
                    {'range': [closed_cmp_perc, 100], 'color': '#3D9970'}]}))

        fig_cv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=300,
                             margin=dict(l=1, r=40, b=15, t=20))
        st.plotly_chart(fig_cv)
        st.markdown(html_card_footer6, unsafe_allow_html=True)
    with col3:
        st.write("")
    with col4:
        st.markdown(html_card_header7, unsafe_allow_html=True)
        fig_sv = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=Inprogrss_cmp_perc, #8th component value 
            number={'suffix': "%","font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': "#06282d"},
                'bgcolor': "white",
                'steps': [
                    {'range': [0, Inprogrss_cmp_perc], 'color': '#FF4136'},
                    {'range': [Inprogrss_cmp_perc, 100], 'color': '#3D9970'}]}))
        fig_sv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=300,
                             margin=dict(l=10, r=10, b=15, t=20))
        st.plotly_chart(fig_sv)
        st.markdown(html_card_footer7, unsafe_allow_html=True)
    with col5:
        st.write("")
    with col6:
        #y = data.loc[data.Activity_name == 'Total']
        #y = data.loc[data.Activity_name == 'Total']
        fig_hh = go.Figure()
        fig_hh.add_trace(go.Bar(
            x=df1['submitted_via'].value_counts().index, #9th component
            y=df1['submitted_via'].value_counts().values
			
            #name='Spend Hours',
            #marker_color='#FF4136'
        ))
#        fig_hh.add_trace(go.Bar(
#            x=df1['submitted_via'].value_counts().index,
#            y=df1['submitted_via'].value_counts().values
            #name='Planned Hours',
            #marker_color='#17A2B8'
#        )) #  8TH COMPONENT
        fig_hh.update_layout(barmode='group', title={'text': 'Submitted Source CMP', 'x': 0.5}, paper_bgcolor="#fbfff0",
                             plot_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Georgia"}, height=250, width=540,
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=0.99,
                                         xanchor="left",
                                         x=0.01),
										 	
                             margin=dict(l=5, r=1, b=1, t=25))
#        fig_hh.update_xaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=6, rangemode="tozero",
#                            showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7')
#        fig_hh.update_yaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=10, rangemode="tozero",
#                            showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7')
        st.plotly_chart(fig_hh)
    with col7:
        st.write("")

html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)

html_subtitle="""
<h2 style="color:#008080; font-family:Georgia;"> Details by Discipline: </h2>
"""
#st.markdown(html_subtitle, unsafe_allow_html=True)

html_table=""" 
<table>
  <tr style="background-color:#eef9ea; color:#008080; font-family:Georgia; font-size: 15px">
    <th style="width:130px">Discipline</th>
    <th style="width:90px">Baseline</th>
    <th style="width:90px">Progress</th>
    <th style="width:90px">Manpower</th>
    <th style="width:90px">Cost Variance</th>
    <th style="width:90px">Schedule Variance</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 14px">
    <th>Civil</th>
    <th>70,00%</th>
    <th>68,50%</th>
    <th>70.000</th>
    <th>0,99</th>
    <th>1,09</th>
  </tr>
  <tr style="background-color:#eef9ea; height: 40px; color:#008080; font-size: 14px">
    <th>Mechanical</th>
    <th>50,00%</th>
    <th>45,50%</th>
    <th>10.000</th>
    <th>0,95</th>
    <th>0,98</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 14px">
    <th>Piping</th>
    <th>30,00%</th>
    <th>30,00%</th>
    <th>60.000</th>
    <th>0,99</th>
    <th>1,01</th>
  </tr>
  <tr style="background-color:#eef9ea; height: 40px; color:#008080; font-size: 14px">
    <th>Electricity</th>
    <th>20,00%</th>
    <th>15,00%</th>
    <th>40.000</th>
    <th>0,90</th>
    <th>0,98</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 14px">
    <th>Intrumentation</th>
    <th>5,00%</th>
    <th>0,00%</th>
    <th>30.000</th>
    <th>-</th>
    <th>-</th>
  </tr>
  <tr style="background-color:#eef9ea; height: 40px; color:#008080; font-size: 14px">
    <th>Commissioning</th>
    <th>0,00%</th>
    <th>0,00%</th>
    <th>15.000</th>
    <th>-</th>
    <th>-</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 15px">
    <th>Total</th>
    <th>35,00%</th>
    <th>46,00%</th>
    <th>225.000</th>
    <th>0,97</th>
    <th>0,91</th>
  </tr>
</table>
"""
































html_line="""
<br>
<br>
<br>
<br>
<hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;">
<p style="color:darkgray; text-align: center;">By: Pardeep Kesnani</p> </center>
"""
st.markdown(html_line, unsafe_allow_html=True)
