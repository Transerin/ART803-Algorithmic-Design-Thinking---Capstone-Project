import pandas as pd
import os
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
from topologicpy.Topology import Topology
from topologicpy.Plotly import Plotly


page_icon = 'Project Icon/icon.ico'
st.set_page_config(page_title='Sønderbrogade 34-40', layout="wide", page_icon=page_icon)
bgcolor = st.get_option("theme.backgroundColor")

# Customize the Streamlit UI: https://towardsdatascience.com/5-ways-to-customise-your-streamlit-ui-e914e458a17c
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

st.title('Building Design')
st.markdown(body='This page could take a while for loading, please be patient.')

# ----------------------------------------------------------------- Part 0 Prepare Topological figure data -----------------------------------------------------------------

# ----------------------------------------------------------------- Part 1 3D Viewer -----------------------------------------------------------------
st.header(f'3D Viewer')

col1, col2 = st.columns(2)
with col1:
    # 3D main structure model viewer
    #st.plotly_chart(topology_fig, use_container_width=True)
    st.markdown(body='This is a Topological model viewer which shows the information of main structures. Please use your cursor to hover over the components to explore.')

with col2:
    # Enscape viewer
    components.iframe(src="https://api2.enscape3d.com/v1/view/0eef3649-2b08-4fac-bbe1-46a8e26373fe", height=800)
    st.markdown(body="This is a Enscape model viewer which shows the design. Due to some cyber security reasons, this iframe doesn't support interaction. However, you can visit [this website](https://api2.enscape3d.com/v1/view/0eef3649-2b08-4fac-bbe1-46a8e26373fe) to get a full-functioned Enscape Web-Viewer. "
                "Alternatively, for the best rendering quality and user experience, you can download an Enscape standalone .exe file [here](https://1drv.ms/u/s!AsPKfnOGCeQVg48ESZhl57QZgD5QcQ?e=8IuapC) and explore it directly from your own PC.")


 # Thematic Break Line
st.markdown('---')


# ----------------------------------------------------------------- Part 2 Room Information -----------------------------------------------------------------
st.header(f'Apartment Information')

# Read data and show room data as DataFrame in Streamlit
plans_image_directory = 'Floor Plans/Plans'
plans_rendering_directory = 'Floor Plans/Renderings'
normal_image_filenames = [filename for filename in os.listdir(plans_image_directory) if filename.endswith('.jpg')]
normal_rendering_filenames = [filename for filename in os.listdir(plans_rendering_directory) if filename.endswith('.jpg')]

def read_data():
    data = pd.read_csv(r'Room Data.csv')
    return data
data = read_data()

# CSS string to hide table row index
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

levels = tuple(data.Levels.unique())

col1, col2 = st.columns(2)
with col1:
    selector = st.selectbox('Levels', levels)
for level in levels:
    if selector == level:
        occupancies = tuple(data.Occupancy[data.Levels == level].sort_values().unique())
        with col2:
            add_selectbox_occupancy = st.selectbox('Occupancy', occupancies)
        for occupancy in occupancies:
            for image_name in normal_image_filenames:
                for rendering_name in normal_rendering_filenames:
                    with open(f'Floor Plans/Plans/{image_name}', 'rb') as f:
                        floor_plan = f.read()
                        clean_image_name = image_name[21:].strip('.jpg')
                    with open(f'Floor Plans/Renderings/{rendering_name}', 'rb') as fr:
                        rendering = fr.read()
                        clean_rendering_name = rendering_name.strip('.jpg')
                    if add_selectbox_occupancy == occupancy and occupancy == clean_image_name and occupancy == clean_rendering_name:
                        col3, col4 = st.columns(2)
                        with col3:
                            st.image(rendering, caption=f'{clean_image_name} Rendering', use_column_width=True)
                        with col4:
                            st.image(floor_plan, caption=f'{clean_image_name} Floor Plan 1:100', use_column_width=True)
                        df = data[(data.Levels == level) & (data.Occupancy == occupancy)].iloc[:,2:7]
                        st.table(df.style.format({'Room Perimeter / m': '{:.2f}', 'Room Area / m²': '{:.2f}', 'Room Volume / m³': '{:.2f}', 'Clear Height / m': '{:.2f}'}))


 # Thematic Break Line
st.markdown('---')

# ----------------------------------------------------------------- Part 3 Technical Drawings -----------------------------------------------------------------
st.header(f'Technical Drawings')

technical_plans_image_directory = 'Floor Plans/Technical Drawings'
technical_plans_image_filenames = [filename for filename in os.listdir(technical_plans_image_directory) if filename.endswith('.jpg')]
clean_technical_plans_image_filenames = [filename.strip('.jpg') for filename in os.listdir(technical_plans_image_directory) if filename.endswith('.jpg')]

with st.expander(label='Control Panel', expanded=True):
    plan_selector = st.selectbox(label='Please select a level to see the detailed technical floor plan.', options=clean_technical_plans_image_filenames, key='technical_floor_plans', index=1)

for tech_fp_name in technical_plans_image_filenames:
    with open(f'Floor Plans/Technical Drawings/{tech_fp_name}', 'rb') as tr:
        tech_fp = tr.read()
        clean_tech_fp_name = tech_fp_name.strip('.jpg')
        if clean_tech_fp_name == plan_selector:
            st.image(image=tech_fp, caption=f'{clean_tech_fp_name} 1:100', use_column_width=True)
            st.download_button(label='Download the technical drawing', data=tech_fp, file_name=f'{tech_fp_name}')
