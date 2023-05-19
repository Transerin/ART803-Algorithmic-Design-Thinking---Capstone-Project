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
############################################################################################################################################################################
# Needs to be developed!!!!! If running locally, remeber to delete all these hashtags
############################################################################################################################################################################
#def read_json(model_file_path, color: str):
    #topologies = Topology.ByJSONPath(model_file_path)
    #topology_data = [Plotly.DataByTopology(topology=topology, showEdges=False, showVertices=False, faceLabelKey='Type Name', faceOpacity=1, faceColor=color) for topology in topologies]
    #return sum(topology_data, [])

#solid_wall_file_path = Path('./3D models/Dynamo for Streamlit/Merged Solid Wall Topological Model.json')
#partition_wall_file_path = Path('./3D models/Dynamo for Streamlit/Merged Partition Wall Topological Model.json')
#roof_file_path = Path('./3D models/Dynamo for Streamlit/Merged Roof Topological Model.json')
#floor_file_path = Path('./3D models/Dynamo for Streamlit/Merged Floor Topological Model.json')
#column_file_path = Path('./3D models/Dynamo for Streamlit/Merged Column Topological Model.json')

#merged_data = read_json(solid_wall_file_path, color='rgb(132, 133, 135)') + read_json(partition_wall_file_path, color='rgb(245, 245, 245)') + read_json(roof_file_path, color='rgb(245, 245, 245)') + read_json(floor_file_path, color='rgb(245, 245, 245)') + read_json(column_file_path, color='rgb(245, 245, 245)')

#topology_fig = Plotly.FigureByData(data=merged_data, height=800)
# ----------------------------------------------------------------- Part 1 3D Viewer -----------------------------------------------------------------
st.header(f'3D Viewer')

col1, col2 = st.columns(2)
with col1:
    # 3D main structure model viewer
    st.markdown(body="This space is intended to display a Topological model viewer, providing detailed insights into the building envelopes. "
               "**:red[However, due to some issues with Streamlit's handling of BREP files, this feature is currently unavailable. In the meantime, this section will remain blank. ]**"
               "If you're interested in viewing the full feature, feel free to clone the repository from GitHub and run the code on your local machine.")
    #st.plotly_chart(topology_fig, use_container_width=True)

with col2:
    # Enscape viewer
    st.markdown(body="Presented here is an Enscape model viewer that showcases the design. However, due to certain cybersecurity constraints, interactive elements within this iframe are unavailable. You can visit [this linked website](https://api2.enscape3d.com/v1/view/0eef3649-2b08-4fac-bbe1-46a8e26373fe) for a fully interactive Enscape Web-Viewer experience. For optimal rendering quality and user engagement, consider downloading the standalone Enscape executable file available [here](https://1drv.ms/u/s!AsPKfnOGCeQVg48ESZhl57QZgD5QcQ?e=8IuapC), allowing you to explore directly from your personal computer.")
    components.iframe(src="https://api2.enscape3d.com/v1/view/0eef3649-2b08-4fac-bbe1-46a8e26373fe", height=800)


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
    plan_selector = st.selectbox(label='Please select a level to see the detailed technical floor plan.', options=clean_technical_plans_image_filenames, key='technical_floor_plans', index=2)

for tech_fp_name in technical_plans_image_filenames:
    with open(f'Floor Plans/Technical Drawings/{tech_fp_name}', 'rb') as tr:
        tech_fp = tr.read()
        clean_tech_fp_name = tech_fp_name.strip('.jpg')
        if clean_tech_fp_name == plan_selector:
            st.image(image=tech_fp, caption=f'{clean_tech_fp_name} 1:100', use_column_width=True)
            st.download_button(label='Download the technical drawing', data=tech_fp, file_name=f'{tech_fp_name}')
