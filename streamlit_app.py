import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Nathan's Frontend ;)")
st.title("Nathan's Frontend ;)")
st.subheader("I'm hungry, feed me an Excel file!")

ExcelFile = st.file_uploader('What is on the menu?', type='xlsx')
if ExcelFile:
  st.markdown('---')
  df = pd.read_excel(ExcelFile, engine='openpyxl')
  st.dataframe(df)
  

if st.button("Fit Lognormal"):
  try:
    
    df['Total'] = df['Paid Indem'] + df['Paid Expense'] + df['OS Indem'] + df['OS Expense']
    df0 = df[df['Total']>0]
    LogLosses = np.array(np.log10(df0['Total']))

    upperLim = np.ceil(np.max(LogLosses))
    step = 0.5
    bins = np.arange(0,upperLim+step,step)
    
    l = []
    h = []
    for loss in LogLosses:
        l.append(loss>=bins[:-1])
        h.append(loss<bins[1:])
    counts = np.sum((np.array(l)*np.array(h)).astype(int),0)
    centers = (bins[:-1]+bins[1:])/2

    def Normal(x,mu,sig):
      return (np.exp(-((x-mu)**2)/(2*sig**2))/np.sqrt(2*np.pi*sig**2))
    mean = np.mean(LogLosses) 
    std = np.std(LogLosses)
    
    st.write("Lognormal Parameters:")
    st.write(r''' $$\mu$$'''+":  "+str(np.round(mean,3))+" , "+r'''$$\sigma$$'''+":  "+str(np.round(std,3)))

    NormBins = np.arange(0,upperLim+step,step/10)
    FittedNormal = Normal(NormBins, mean, std)

    fig = plt.figure(figsize=(8,5))
    plt.plot(NormBins, FittedNormal, color="purple")
    plt.bar(centers, counts/np.sum(counts)*2, width=0.4)
    plt.xlabel('Log10(Losses)')
    plt.ylabel('Probabliltiy Density')
    plt.legend(['Fit','Data'])
    plt.title('A nice little graph')
    st.pyplot(fig)
    
  except:
    st.write("You have to feed me first!")
