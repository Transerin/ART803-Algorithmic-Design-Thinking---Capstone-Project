from pathlib import Path
import streamlit as st
import pandas as pd
from ladybug.color import Colorset, Color
from pollination_streamlit_viewer import viewer
from ladybug_vtk.visualization_set import VisualizationSet
from ladybug_display.visualization import VisualizationSet as LBVisualizationSet

views = [
          '',
          'Top',
          'Bottom',
          'Left',
          'Right',
          'Front',
          'Back'
        ]

colorsets = {
    'Original': Colorset.original(),
    'Nuanced': Colorset.nuanced(),
    'Ecotect': Colorset.ecotect(),
    'Energy_balance': Colorset.energy_balance(),
    'Energy_balance_storage': Colorset.energy_balance_storage(),
    'Multi_colored': Colorset.multi_colored(),
    'Multicolored_2': Colorset.multicolored_2(),
    'Multicolored_3': Colorset.multicolored_3(),
    'Openstudio_palette': Colorset.openstudio_palette(),
    'Shade_harm': Colorset.shade_harm(),
    'Therm': Colorset.therm(),
    'View_study': Colorset.view_study()
}


page_icon = 'Project Icon/icon.ico'
st.set_page_config(page_title='Sønderbrogade 34-40', layout="wide", page_icon=page_icon)
bgcolor = st.get_option("theme.backgroundColor")


# Transform a Pollination Visualization Set file to a .vtkjs file
# https://www.ladybug.tools/ladybug-vtk/docs/ladybug_vtk.visualization_set.html
@st.cache_data
def transform_vsf_to_vtkjs(file_path: Path, folder_path: Path):
    lb_vs = LBVisualizationSet.from_file(file_path)
    name = str(file_path).strip('.vsf')
    return VisualizationSet.from_visualization_set(lb_vs).to_vtkjs(folder=folder_path, name=name)

daylight_factor_path = 'Pollination Visual_Set/Daylight Factor.vsf'
annual_daylight_path = 'Pollination Visual_Set/Annual Daylight.vsf'

folder_path = Path('')
daylight_factor_vtkjs = Path(transform_vsf_to_vtkjs(file_path=daylight_factor_path, folder_path=folder_path)).read_bytes()
annualy_daylight_vtkjs = Path(transform_vsf_to_vtkjs(file_path=annual_daylight_path, folder_path=folder_path)).read_bytes()

# Customize the Streamlit UI: https://towardsdatascience.com/5-ways-to-customise-your-streamlit-ui-e914e458a17c
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

st.title("Visualize Daylight Analysis")
st.markdown('💡 **Please note that if you encountered some glitches with the renderer, for instance, the 3D viewer is displaying in gray, please use your cursor to interact '
            'with it, such as zoom in, zoom out or right click, any interations, to bring back the viewer.**')


if 'action_stack' not in st.session_state:
    st.session_state.action_stack = []

def handle_colorset():
    if 'colorset_select' in st.session_state:
        st.session_state.action_stack.append({
            'type': 'color-set',
            'value': st.session_state.colorset_select
        })
      
def handle_views():
    if 'views' in st.session_state:
        st.session_state.action_stack.append({
            'type': 'select-view',
            'value': st.session_state.views.lower()
        })
    if 'toggle_ortho' in st.session_state:
        st.session_state.toggle_ortho = True
        st.session_state.action_stack.append({
            'type': 'toggle-ortho',
            'value': st.session_state.toggle_ortho
        })

def handle_resetcamera():
    if 'reset_camera' in st.session_state:
        st.session_state.action_stack.append({
            'type': 'reset-camera',
            'value': st.session_state.reset_camera
        })
        
def handle_toggleortho ():
  if 'toggle_ortho' in st.session_state:
    st.session_state.action_stack.append({
      'type': 'toggle-ortho',
      'value': st.session_state.toggle_ortho
    })

def handle_screenshot ():
  st.session_state.action_stack.append({
    'type': 'streamlit-screenshot'
  })
  


with st.expander(label='Control Panel', expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox('Global Colorsets Selector', colorsets.keys(), key='colorset_select', on_change=handle_colorset, help="If you don't like the predefined colorset, you can use this selector to change the colorset.")
    with col2:
        st.selectbox('Select an Orthogonal View', views, key='views', index=0, on_change=handle_views)
        col3, col4, col5, col6 = st.columns([1, 1, 2, 1])
        with col3:
            st.button('Reset camera', key='reset_camera', on_click=handle_resetcamera)
        with col4:
            st.button('Screenshot', key='streamlit-screenshot', on_click=handle_screenshot)
        with col5:
            st.checkbox('Toggle Orthographic / Perspective', value=False, key='toggle_ortho', on_change=handle_toggleortho)
        with col6:
            st.checkbox('Sidebar', value=False, key='sidebar_toggle', help='Show/Hide the side toolbar.')

tabs = st.tabs(['Daylight Factor Analysis', 'Annual Daylight Analysis'])
with tabs[0]:
    df_vtkjs = viewer(key='daylight_factor', content=daylight_factor_vtkjs, sidebar=st.session_state.sidebar_toggle, action_stack=st.session_state.action_stack)
    
     # Thematic Break Line
    st.markdown('---')
    
    st.header('Terminology')
    # https://docs.ladybug.tools/hb-radiance-primer/components/3_recipes/daylight_factor
    st.markdown('Daylight Factor (DF) is defined as the ratio of the indoor daylight illuminance to outdoor illuminance under an unobstructed overcast sky. It is expressed as a percentage between 0 and 100.')

with tabs[1]:
    ad_vtkjs = viewer(key='annual_dalight', content=annualy_daylight_vtkjs, sidebar=st.session_state.sidebar_toggle, action_stack=st.session_state.action_stack)
        
     # Thematic Break Line
    st.markdown('---')
    
    st.header('Terminology')
    # https://docs.ladybug.tools/hb-radiance-primer/components/3_recipes/annual_daylight
    st.markdown('This recipe uses an enhanced 2-phase method for daylight simulation which accurately models direct sun by tracing rays from each sensor to the solar position at each hour of the calculation. The resulting illuminance is used to compute the following metrics: **Daylight Autonomy (DA)** - The percentage of occupied hours that each sensor recieves more than the illuminance threshold. **Continuous Daylight Autonomy (cDA)** - Similar to DA except that values below the illuminance threshold can still count partially towards the final percentage. **Useful Daylight Illuminance (UDI)** - The percentage of occupied hours that illuminace falls between minimum and maximum thresholds')

st.session_state.action_stack.clear()
           

