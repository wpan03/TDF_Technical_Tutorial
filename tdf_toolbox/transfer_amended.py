import pandas as pd 
import base64
import streamlit as st

#Functions for extracting id from stage 1 spreadsheet
def get_amend(file_name, sheets):
    store = []

    for i in range(len(sheets)):
        if i == 0:
            df = pd.read_excel(file_name, sheet_name=sheets[i], skiprows=[0])
            for i in list(df.columns):
                if 'Amended' in i:
                    select1 = i
            df_select = df[[select1]]
            df_select.columns = ['Projects Amended']
        elif i == 1:
            df = pd.read_excel(file_name, sheet_name=sheets[i])
            for i in list(df.columns):
                if 'Existing' in i:
                    select2 = i
            df_select = df[[select2]]
            df_select.columns = ['Projects Amended']
        elif i >= 2:
            df = pd.read_excel(file_name, sheet_name=sheets[i])
            for i in list(df.columns):
                if 'Amend' in i:
                    select3 = i
            df_select = df[[select3]]
            df_select.columns = ['Projects Amended']

        store.append(df_select)

    df = pd.concat(store).dropna().reset_index(drop=True)

    #break projects in one cell to one project per row 
    df['Projects Amended'] = df['Projects Amended'].astype(str)
    special = df['Projects Amended'].str.split(',').notnull()
    df.loc[special, 'Projects Amended'] = df[special]['Projects Amended'].str.split(',')
    df = df.explode('Projects Amended')

    df['Projects Amended'] = df['Projects Amended'].astype(str)
    special1 = df['Projects Amended'].str.strip().notnull()
    df.loc[special1, 'Projects Amended'] = df[special1]['Projects Amended'].str.strip()

    df_clean = df.drop_duplicates('Projects Amended').reset_index(drop=True)
    return df_clean

def transfer_amend():

    #Title and file upload
    st.header('Transfer Amended OCP Project')
    ocp_amend_requirement  = st.checkbox('ocp amend requirment')
    if ocp_amend_requirement:
        st.markdown("+ The tab in the excel file should have following order: General Tab, Project List, and Year Tab.")
        st.markdown("+ There should be one line above the header in the general tab")
        st.markdown("+ There should be no line above the header in the project list and year tab")

    stage1 = st.file_uploader("Choose a the stage 1 excel file", type="xlsx")
    stage2 = st.file_uploader("Choose a stage 2 excel file", type = "xlsx")


    if (stage1 != None) and (stage2 != None):
        
        all_sheet = pd.ExcelFile(stage1)   
        sheets = all_sheet.sheet_names

        #Read Stage 2 Spreadsheet 
        all_stage2_sheet = pd.ExcelFile(stage2)
        stage2_sheet = st.selectbox('Which tab in the stage 2 spreadsheet?', all_stage2_sheet.sheet_names)
        df_st2 = pd.read_excel(stage2, sheet_name= stage2_sheet)
        df_st2.columns = df_st2.columns.str.lower()
        country = st.selectbox('Which Country?', df_st2['country'].unique())
  
        if st.button('Start Transfer!'):

            #Run the function
            file_name = stage1
            df_amend = get_amend(file_name, sheets)

            #Get rid of repeated id in stage 2
            id = [s for s in list(df_st2.columns) if "id" in s][0]
            stage2_list = df_st2[df_st2['country'] == country][id].reset_index(drop=True).astype(str)
            df_not_repeat = df_amend[~df_amend['Projects Amended'].isin(stage2_list)].reset_index(drop=True)

            #Export spread sheet
            df_not_repeat['Source'] = 'OCP'
            df_not_repeat['Country'] = country

            def get_table_download_link(df):
                """Generates a link allowing the data in a given panda dataframe to be downloaded
                in:  dataframe
                out: href string"""
                    
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(
                csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

            st.markdown(get_table_download_link(df_not_repeat), unsafe_allow_html=True)    
            st.text('Congratulations!')
            st.text('You get rid of {} repeated projects'.format(df_amend.shape[0]-df_not_repeat.shape[0]))
            st.text("You finally transferred about {} projects".format(df_not_repeat.shape[0]))