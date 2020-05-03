import pandas as pd
import streamlit as st
import base64

def merge():
    st.header('Merge according to project id')
    export_file = st.file_uploader("Choose an exported csv file", type="csv")
    stage2_file = st.file_uploader('Choose the stage 2 excel file', type = 'xlsx')
    
    if (export_file != None) and (stage2_file != None):
        stage2_sheet = pd.ExcelFile(stage2_file)
        sheet = st.selectbox('Which tab in the stage 2 spreadsheet?', stage2_sheet.sheet_names)
        df_stage2 = pd.read_excel(stage2_file, sheet_name=sheet)
        df_export = pd.read_csv(export_file)

        df_stage2.columns = df_stage2.columns.str.strip()
        id = [s for s in list(df_stage2.columns) if "id" in s.lower()][0]

        country = st.selectbox('Which country?', df_stage2['Country'].unique())
        df_stage2 = df_stage2[df_stage2['Country'] == country]
        
        

    
        left_identifier = st.text_input('stage 2 identifier', value=id)
        right_identifier = st.text_input('export identifier', value = 'project_id')
        how_to_merge = st.text_input('how to merge', value = 'left')

        if st.button('merge'):
            df_merge = pd.merge(df_stage2, df_export, left_on=left_identifier, right_on=right_identifier, how=how_to_merge)
        
            def get_table_download_link(df):
                    """Generates a link allowing the data in a given panda dataframe to be downloaded
                    in:  dataframe
                    out: href string"""
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(
                    csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

            selections = ['project_id','year','flow_class','Country']
            df_merge = df_merge[selections]
            st.markdown(get_table_download_link(df_merge), unsafe_allow_html=True)    
