import streamlit as st
import pandas as pd
import webbrowser

def search_duplicate(): 
  st.title('Search Duplicate')

  uploaded_file = st.file_uploader("Choose a export csv file", type="csv")

  if uploaded_file != None:
    df = pd.read_csv(uploaded_file)
    df['year'] = df.year.fillna(0)

    def filter_search(df, keyword, year_min=2000, year_max=2019, donor='China', Active=True):
        df = df[(df['year'] >= year_min) | (df['year'] == 0)]
        df = df[(df['year'] <= year_max) | (df['year'] == 0)]
        df = df[df['donor'] == donor]
        if Active is True:
            df = df[df['active'] == 'Active']
        result = df[df['description'].str.contains(keyword, na=False, case=False)| df['title'].str.contains(keyword, na=False, case=False)].reset_index(drop=True)
        return result


    base = r'^{}'
    expr = '(?=.*{})'
    text_input = st.text_input('keyword', value='None')
    words = text_input.split(" ")
    search_input = base.format(''.join(expr.format(w) for w in words))

    active = False
    if st.checkbox('Only Active'):
        active = True

    year_min_max = st.slider('year', 2000, 2019, value=[2000, 2019])
    year_min = year_min_max[0]
    year_max = year_min_max[1]


    # Otherwise, 'a|b' will search strings that contain a or b
    result = filter_search(df, keyword=search_input, year_min=year_min, year_max=year_max, Active = active)
    result = result.sort_values('year').reset_index(drop=True)

    # Display Project_id, title, year
    st.subheader('Search Results')
    st.table(result[['project_id', 'year', 'title']])

    # See the description
    if st.checkbox('get description'):
        index = st.number_input('which one', value=-1)
        if index != -1:
            st.write(result.loc[index]['description'])

  # See the project in our website
  if st.checkbox('open project in aiddata website'):
      project_id = st.number_input('project_id', value = 0)
      if project_id != 0:
          st.markdown("[Open Project](http://admin.china.aiddata.org/projects/{})".format(project_id))

  st.subheader('Useful Sources')

  st.markdown("[TUFF 1.4 Guide](https://docs.google.com/document/d/1henyi4ixkRKMSH4k2Is9g-N5T8GeBWgEOINDzSaLE4c/edit)")
  st.markdown("[CRS Sector](https://www.oecd.org/dac/stats/documentupload/Budget%20identifier%20purpose%20codes_EN_Apr%202016.pdf)")
  st.markdown("[Google Translate](https://translate.google.com/)")
  st.markdown("[LIBOR](https://www.global-rates.com/interest-rates/libor/american-dollar/2017.aspx)")

