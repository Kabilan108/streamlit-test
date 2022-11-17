"""
Streamlit Demo: Volcano Plots
"""

# Imports
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

st.title("Plotly Volcano Plots")

DATA_URL = ("https://raw.githubusercontent.com/plotly/datasets/master/Dash_Bio/"
            "Chromosomal/volcano_data1.csv")


@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    data['-log10(p)'] = -np.log10(data['P'])
    data['EFFECTSIZE'] = 2 * data['EFFECTSIZE']
    return data


# Load data
data_load_state = st.text('Loading data ...')
data = load_data()
data_load_state.text("Done!")

st.subheader('Differential Gene Expression')

# Sliders
pval = st.slider('p-Value Threshold', 0.00, 0.10, 0.05)
neglogpval = -np.log10(pval)
fc = st.slider('Effect Size Threshold', 0.5, 3.0, 2.0)

# Split the data
I = (data['P'] <= pval) & ((data['EFFECTSIZE'] >=fc) | (data['EFFECTSIZE'] <= -fc))
nonsig = data.loc[~I, :]
sig = data.loc[I, :]

# Create figure
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=nonsig['EFFECTSIZE'],
        y=nonsig['-log10(p)'],
        marker=dict(
            color='gray'
        ),
        mode='markers',
        name='Non Significant'
    )
)
fig.add_trace(
    go.Scatter(
        x=sig['EFFECTSIZE'],
        y=sig['-log10(p)'],
        marker=dict(
            color='red'
        ),
        mode='markers',
        name='Significant'
    )
)
fig.add_hline(y=neglogpval, line_dash='dash', annotation_text=f'p = {pval}')
fig.add_vline(x=fc, line_dash='dash')
fig.add_vline(x=-fc, line_dash='dash')


st.plotly_chart(fig, use_container_width=True)

st.subheader('Raw Data')
st.write(data)

#st.subheader('Number of pickups by hour')
#hist_values  = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#st.bar_chart(hist_values)

#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour== hour_to_filter]

#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)
