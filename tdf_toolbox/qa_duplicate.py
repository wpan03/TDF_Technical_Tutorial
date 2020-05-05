import pandas as pd
import streamlit as st
import base64

def find_repeat():
    st.header('Find Repeated Projects in QA Amended and Stage 2')
    st.text('Note that this program currently keeps not repeated projects in the ameneded projects.')
    qa_file = st.file_uploader("Choose a qa excel file", type="xlsx")
    stage2_file = st.file_uploader('Choose the stage 2 excel file', type = 'xlsx')
    
    if (qa_file != None) and (stage2_file != None):
        stage2_sheet = pd.ExcelFile(stage2_file)
        st2_sheet = st.selectbox('Which tab in the stage 2 spreadsheet?', stage2_sheet.sheet_names)
        df_stage2 = pd.read_excel(stage2_file, sheet_name=st2_sheet)

        qa_sheet = pd.ExcelFile(qa_file)
        qa_sheet = st.selectbox('Which tab in the qa spreadsheet?', qa_sheet.sheet_names)
        df_qa = pd.read_excel(qa_file, sheet_name= qa_sheet)

        country = st.selectbox('Which country?', df_stage2['Country'].unique())
        df_stage2 = df_stage2[df_stage2['Country'] == country]
        df_qa = df_qa[df_qa['Country'] == country]
        
        df_stage2.columns = df_stage2.columns.str.strip()
        st2_id = [s for s in list(df_stage2.columns) if "id" in s.lower()][0]
        qa_id = [x for x in list(df_qa.columns) if "id" in x.lower()][0]
        
        target_stage2 = df_stage2[st2_id].reset_index(drop=True)
        not_repeat = df_qa[~df_qa[qa_id].isin(target_stage2)][qa_id].reset_index(drop=True)
        repeat = df_qa[df_qa[qa_id].isin(target_stage2)][qa_id].reset_index(drop=True)

        if st.button('Get not repeated projects'):
            
        
            def get_table_download_link(df):
                    """Generates a link allowing the data in a given panda dataframe to be downloaded
                    in:  dataframe
                    out: href string"""
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(
                    csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

            st.markdown(get_table_download_link(not_repeat), unsafe_allow_html=True)
            st.text('We found {} repeated projects, they are:'.format(df_qa.shape[0]-not_repeat.shape[0]))
            st.write(repeat)
