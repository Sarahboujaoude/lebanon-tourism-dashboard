import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lebanon Tourism Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("tourism.csv")
    def clean_ref_area(val):
        val = str(val).split('/')[-1]
        val = val.replace('_', ' ').replace('-Governorate', '').replace('District', '').replace(', Lebanon', '')
        return val.strip()
    df['Clean_Region'] = df['refArea'].apply(clean_ref_area)
    return df

df = load_data()

st.title("🇱🇧 Lebanon Tourism & Hospitality Infrastructure")
st.markdown("This dashboard explores regional distribution patterns across Lebanon's tourism and hospitality infrastructure.")

st.sidebar.header("🗺️ Filter Controls")
regions = sorted(df['Clean_Region'].unique().tolist())
selected_region = st.sidebar.selectbox("1. Select Region / District", options=regions)

filtered_df = df[df['Clean_Region'] == selected_region]
available_towns = sorted(filtered_df['Town'].unique().tolist())

st.sidebar.markdown(f"**2. Select Towns in {selected_region}:**")
selected_towns = []
select_all = st.sidebar.checkbox("Select All in Region", value=True)

for town in available_towns:
    if select_all:
        is_checked = st.sidebar.checkbox(town, value=True, key=f"{selected_region}_{town}")
    else:
        is_checked = st.sidebar.checkbox(town, value=False, key=f"{selected_region}_{town}")
    if is_checked:
        selected_towns.append(town)

if selected_towns:
    plot_df = filtered_df[filtered_df['Town'].isin(selected_towns)]
else:
    plot_df = filtered_df

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hotels vs. Restaurants")
    if not plot_df.empty:
        melted_df = plot_df.melt(id_vars=['Town'], value_vars=['Total number of hotels', 'Total number of restaurants'], var_name='Facility Type', value_name='Count')
        melted_df['Facility Type'] = melted_df['Facility Type'].str.replace('Total number of ', '')
        fig1 = px.bar(melted_df, x='Town', y='Count', color='Facility Type', barmode='group', title=f"Hotels vs Restaurants in {selected_region}", template='plotly_white')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Please select at least one town.")

with col2:
    st.subheader("Cafe Density")
    if not plot_df.empty:
        fig2 = px.bar(plot_df, x='Town', y='Total number of cafes', title=f"Cafe Distribution in {selected_region}", color='Total number of cafes', color_continuous_scale='Viridis', template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Please select at least one town.")

with st.expander("📝 View Design Justifications"):
    st.markdown("""
    #### 1. Region / District Dropdown (`st.selectbox`)
    * **User Question:** Which broad geographical region or district does the user want to focus the analysis on?
    * **Widget Choice:** A dropdown was chosen because it cleanly handles single-choice categorical boundaries without cluttering the sidebar.
    * **Course Concept:** It establishes macro-level context and sets a clear spatial boundary.

    #### 2. Linked Town Checkboxes (`st.checkbox`)
    * **User Question:** Which specific towns within the chosen region should be included in the visualizations?
    * **Widget Choice:** Checkboxes provide an intuitive binary toggle mechanism that updates charts instantly.
    * **Course Concept:** It aligns with focusing attention and reducing clutter by dynamically generating options relative to the parent dropdown.
    """)
