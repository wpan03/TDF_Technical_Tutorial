import pandas as pd
import streamlit as st

def examine():
    st.title('Examine Projects in a Country')
    st.text('We only keep active official finance projects.')
    
    uploaded_file = st.file_uploader("Choose an export csv file", type="csv")

    if uploaded_file != None:

        df = pd.read_csv(uploaded_file)
        official_selection = df['flow_class'].isin(['ODA-like','OOF-like','Vague (Official Finance)'])
        df_of = df[official_selection]
        active_selection = (df_of['active'] == 'Active')
        df_of_active = df_of[active_selection]

        st.header('Summary Statistics')
        st.subheader('Flow Class')
        st.write(df_of_active['flow_class'].value_counts())
        

        st.header('Potential Coding Errors')

        st.subheader('Project without donor agency')
        no_donor_agency = df_of_active['donor_agency'].isnull()
        df_no_donor_agency = df_of_active[no_donor_agency][['project_id','year','title']].reset_index(drop=True)
        st.table(df_no_donor_agency)

        st.subheader('Project without development intent but with ODA flow class')
        oda_not_development = (df_of_active['intent'] != 'Development') & (df_of_active['flow_class'] == 'ODA_like')
        df_oda_not_development = df_of_active[oda_not_development]
        st.table(df_oda_not_development)
    
    
    
    