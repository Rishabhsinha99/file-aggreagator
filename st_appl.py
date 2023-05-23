
import streamlit as st
import pandas as pd
import numpy as np

repl_dict={'Y':"Yes","y":"Yes","yes":"Yes","YES":"Yes","Yes":"Yes",
           "N":"No","no":"No","NO":"No","n":"No","No":"No",
           np.NaN:"Blank"}

#%%

uploaded_file = st.file_uploader("Choose the file in requisite format")
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file,sheet_name="Master sheet",header=1)
    df=df.dropna(how='all')
    key=pd.read_excel("DoT_List of Competencies.xlsx",sheet_name='Domain')

else:
    st.warning('Please Upload File')


df['(L1)']=df['(L1)'].apply(lambda x:repl_dict[x])
df['(L2)']=df['(L2)'].apply(lambda x:repl_dict[x])
df['(L3)']=df['(L3)'].apply(lambda x:repl_dict[x])
df['(L4)']=df['(L4)'].apply(lambda x:repl_dict[x])

l1=pd.crosstab(df['Code '],df['(L1)'])
l1.columns=["L1_"+x for x in l1.columns]
l2=pd.crosstab(df['Code '],df['(L2)'])
l2.columns=["L2_"+x for x in l2.columns]
l3=pd.crosstab(df['Code '],df['(L3)'])
l3.columns=["L3_"+x for x in l3.columns]
l4=pd.crosstab(df['Code '],df['(L4)'])
l4.columns=["L4_"+x for x in l4.columns]

l1.reset_index(inplace=True)
l2.reset_index(inplace=True)
l3.reset_index(inplace=True)
l4.reset_index(inplace=True)


level_breakdown=((l1.merge(l2)).merge(l3)).merge(l4)
level_breakdown.rename(columns={'Code ':"Code"},inplace=True)

#%%

req=df['Code '].value_counts().reset_index()
req.columns=['Code','# Count']
req['Code']=req['Code'].astype(int,errors='ignore')

#%%

exp=req.merge(level_breakdown)

for i in range(len(exp)):
    try:
        exp.loc[i,'Code']=int(exp.loc[i,'Code'])
    except:
        continue

key=key[['S. No.','Competency Name']].drop_duplicates()
key.columns=['Code','Domain Competency Name']
final_df=key.merge(exp,how='right')

st.markdown("\n\n")
st.dataframe(final_df,use_container_width=True)

#%%

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

converted_df = convert_df(final_df)

st.download_button("Click to Download the aggregated table",converted_df,
                   file_name="Count File.csv",mime='text/csv')











