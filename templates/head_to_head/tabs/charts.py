import streamlit as st
import matplotlib.pyplot as plt


def bar_chart(title, df):
    """Create a bar chart"""
    # Create the bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df[''], df['Records'])
    ax.set_ylabel("Records")
    ax.set_title(title)

    # Display the chart in Streamlit
    st.pyplot(fig)
