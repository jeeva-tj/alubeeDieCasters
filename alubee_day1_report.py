import streamlit as st
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from datetime import datetime
import pytz
import plotly.graph_objects as go
import plotly.express as px




st.set_page_config(layout="wide")
column1,column2,column3,column4,column5,column6,column7,column8 = st.columns(8)

with column1:

    st.markdown('<div style="display:flex; align-items:center;"><img src="https://storage.cloud.google.com/alubee_bucket/biglogo.png?authuser=4" style="width:80px;height:50px;margin-right:20px;" />', unsafe_allow_html=True)

with column8:

    st.markdown('<div style="margin-bottom: 10px;"><h7 class="title">Date  : 24 Sept 2023  Shift : II</h7></div>', unsafe_allow_html=True)
    # st.markdown('<div style="margin-bottom: 10px;"><h7 class="title">Shift : II</h7></div>', unsafe_allow_html=True)


url = "https://us-central1-1.gcp.cloud2.influxdata.com"
token = "7vu3JRiROx0LRI6P24ze8FfONTrRgVA_PKlTrVsW_ho2wt3v9GgWNTRGRsELZSyOkMA_rQaynNJQMs6-OENbEA=="
org = "dev"
bucket = "alubee_master_table"

client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

query = f'from(bucket:"{bucket}") |> range(start:2023-09-23T14:30:00.00Z , stop:2023-09-24T02:30:00.00Z) |> filter(fn: (r) => r["_measurement"] == "Shot")'
tables = client.query_api().query(query, org=org)

data_list = []

for table in tables:
    for row in table.records:
        data = row.values
        # Convert UTC time to IST
        utc_time = data['_time']
        ist = pytz.timezone('Asia/Kolkata')
        data['_time'] = utc_time.astimezone(ist)
        data_list.append(data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data_list)

columns_to_drop = ['result', '_start','_stop','_field']  # List of columns to drop

df = df.drop(columns=columns_to_drop)

df['_time'] = df['_time'].dt.floor('H') + pd.Timedelta(hours=1)

df_grouped = df.groupby('_time').agg({'_value': 'sum'}).reset_index()

column1,column2= st.columns(2)

with column1:

    st.markdown("")
    st.markdown("")

column_fir1,column_fir2,column_fir3,column_fir4,column_fir5= st.columns(5)

with column_fir1:
    st.metric(label="Total Shots", value=df_grouped["_value"].sum(), delta=0,delta_color="off")



column1,column2 = st.columns(2)

with column1:

    fig = px.bar(df_grouped, y='_value', x='_time', text_auto='.2s',
                title="Shots Per Hour",color_discrete_sequence=['#00a651'])
    # fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
    fig.update_xaxes(title='Time in Hour')
    fig.update_yaxes(title='No of Shots')
    fig.update_layout(height=400, width=600)

    st.plotly_chart(fig)





#----------------------------Rejection---------------------------------------------

query = f'from(bucket:"{bucket}") |> range(start:2023-09-23T14:30:00.00Z , stop:2023-09-24T02:30:00.00Z) |> filter(fn: (r) => r["_measurement"] == "Rejection")'
tables = client.query_api().query(query, org=org)

# Initialize an empty list to store dictionaries
data_list = []

for table in tables:
    for row in table.records:
        data = row.values
        # Convert UTC time to IST
        utc_time = data['_time']
        ist = pytz.timezone('Asia/Kolkata')
        data['_time'] = utc_time.astimezone(ist)
        data_list.append(data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data_list)

columns_to_drop = ['result', '_start','_stop','_field']  # List of columns to drop

df = df.drop(columns=columns_to_drop)
df['_time'] = df['_time'].dt.floor('H') + pd.Timedelta(hours=1)

# Group by hourly intervals and sum shots
df_grouped = df.groupby('_time').agg({'_value': 'sum'}).reset_index()
# st.dataframe(df_grouped)

with column2:
  
    fig = px.line(df_grouped, x='_time', y="_value",title="Rejections Per Hour",color_discrete_sequence=['#767a79'])
    # fig = px.bar(df_grouped, x='_time', y='_value',
    #             color='_value',
    #             labels={'pop':'Rejection Count'}, height=400)
    fig.update_xaxes(title='Time in Hour')
    fig.update_yaxes(title='No of Rejections')
    fig.update_traces(text=df_grouped['_value'], mode='lines+markers+text', textposition='top center')
    fig.update_layout(height=400, width=600)

    st.plotly_chart(fig)



with column_fir2:
    st.metric(label="Total Rejections", value=df_grouped["_value"].sum(), delta=0,delta_color="off")







# # Header
# st.header("This is a header")

# # Subheader
# st.subheader("This is a subheader")

# # Text
# st.write("This is some plain text.")

# # Markdown
# st.markdown("### This is a Markdown header")

# # Displaying a number
# number = st.number_input("Enter a number", min_value=0, max_value=100)

# # Displaying a slider
# slider_value = st.slider("Choose a value", min_value=0, max_value=100)

# # Button
# if st.button("Click me"):
#     st.write("Button clicked!")

# # Checkbox
# checkbox = st.checkbox("Checkbox")
# if checkbox:
#     st.write("Checkbox is checked")

# # Selectbox
# option = st.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
# st.write("You selected:", option)

# # Radio button
# radio = st.radio("Choose one option", ["Option A", "Option B", "Option C"])
# st.write("You selected:", radio)
