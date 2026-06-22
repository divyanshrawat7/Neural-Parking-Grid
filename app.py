import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="AI Parking Intelligence", layout="wide")

st.markdown("""
    <style>
    /* --- HIDE STREAMLIT DEFAULT UI (Deploy Button & Menu) --- */
    [data-testid="stDeployButton"] {display: none !important;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main Background & Text */
    .stApp { background-color: #0A0A0E; color: #E0E0E0; font-family: 'Courier New', Courier, monospace; }
    
    /* Headers - Neon Cyan Glow */
    h1, h2, h3 { color: #00F0FF !important; text-shadow: 0px 0px 8px rgba(0, 240, 255, 0.6); font-weight: 700; letter-spacing: 1px; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #121218; border-right: 1px solid #39FF14; }
    
    /* Metric Cards - Glowing Borders */
    [data-testid="stMetricValue"] { color: #FF007F !important; text-shadow: 0px 0px 10px rgba(255, 0, 127, 0.8); font-size: 2.5rem !important; }
    [data-testid="stMetricLabel"] { color: #00F0FF !important; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Dataframe styling */
    .stDataFrame { border: 1px solid #00F0FF; box-shadow: 0 0 10px rgba(0, 240, 255, 0.2); }
    
    /* Horizontal Rule */
    hr { border-color: rgba(0, 240, 255, 0.3); }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def process_raw_data(file_buffer):
    df = pd.read_csv(file_buffer)
    
    df['created_datetime'] = pd.to_datetime(df['created_datetime'], format='ISO8601', utc=True, errors='coerce')
    parking_mask = df['violation_type'].str.contains('PARKING', case=False, na=False)
    parking_df = df[parking_mask].copy()
    
    if parking_df.empty: return pd.DataFrame(), []
        
    parking_df['hour'] = parking_df['created_datetime'].dt.hour
    parking_df['grid_lat'] = parking_df['latitude'].round(4)
    parking_df['grid_lon'] = parking_df['longitude'].round(4)
    
    
    heat_data = parking_df[['latitude', 'longitude']].dropna().values.tolist()
    
    grid_summary = parking_df.groupby(['grid_lat', 'grid_lon']).agg(
        violation_count=('id', 'count'),
        primary_police_station=('police_station', lambda x: x.mode()[0] if not x.empty else 'Unknown')
    ).reset_index()
    
    dense_grids = grid_summary[grid_summary['violation_count'] >= 5].copy()
    if dense_grids.empty: return pd.DataFrame(), heat_data
        
    coords = np.radians(dense_grids[['grid_lat', 'grid_lon']].values)
    db = DBSCAN(eps=0.0005, min_samples=2, algorithm='ball_tree', metric='haversine')
    dense_grids['hotspot_cluster_id'] = db.fit_predict(coords)
    hotspots = dense_grids[dense_grids['hotspot_cluster_id'] != -1]
    
    final_summary = hotspots.groupby('hotspot_cluster_id').agg(
        total_violations_in_zone=('violation_count', 'sum'),
        center_lat=('grid_lat', 'mean'),
        center_lon=('grid_lon', 'mean'),
        jurisdiction=('primary_police_station', lambda x: x.mode()[0])
    ).reset_index()
    
    parking_with_clusters = pd.merge(parking_df, hotspots[['grid_lat', 'grid_lon', 'hotspot_cluster_id']], on=['grid_lat', 'grid_lon'], how='inner')
    parking_with_clusters['is_near_junction'] = ~parking_with_clusters['junction_name'].isin(['No Junction', 'NaN', 'nan']) & parking_with_clusters['junction_name'].notna()
    
    impact_stats = parking_with_clusters.groupby('hotspot_cluster_id').agg(
        junction_violations=('is_near_junction', 'sum'),
        peak_hour=('hour', lambda x: x.mode()[0] if not x.empty else -1)
    ).reset_index()
    
    final_hotspots = pd.merge(final_summary, impact_stats, on='hotspot_cluster_id', how='left')
    final_hotspots['congestion_impact_score'] = final_hotspots['total_violations_in_zone'] + (final_hotspots['junction_violations'] * 2.5)
    
    final_hotspots = final_hotspots.sort_values('congestion_impact_score', ascending=False).reset_index(drop=True)
    return final_hotspots, heat_data


st.sidebar.markdown("### SYSTEM OVERRIDE")
uploaded_file = st.sidebar.file_uploader("UPLOAD RAW TELEMETRY [CSV]", type="csv")

if uploaded_file is not None:
    with st.spinner("DECRYPTING DATA & EXECUTING SPATIAL CLUSTERING"):
        df, heat_data = process_raw_data(uploaded_file)

    if not df.empty:
        jurisdictions = ["ALL ZONES"] + list(df['jurisdiction'].unique())
        selected_jurisdiction = st.sidebar.selectbox("GLOBAL JURISDICTION FILTER:", jurisdictions)

        if selected_jurisdiction != "ALL ZONES":
            filtered_df = df[df['jurisdiction'] == selected_jurisdiction]
        else:
            filtered_df = df

        
        st.title("NEURAL PARKING & CONGESTION GRID")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("CRITICAL HOTSPOTS", len(filtered_df))
        col2.metric("MAPPED VIOLATIONS", int(filtered_df['total_violations_in_zone'].sum()))
        col3.metric("JUNCTION THREATS", int(filtered_df['junction_violations'].sum()))
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h4 style='color: #00F0FF; font-family: monospace;'>>> REAL-TIME THREAT ANALYTICS</h4>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.caption("JURISDICTION IMPACT SCORES")
            bar_data = filtered_df[['jurisdiction', 'congestion_impact_score']].set_index('jurisdiction')
            st.bar_chart(bar_data, color="#FF007F")
            
        with chart_col2:
            st.caption("HOTSPOT PEAK ACTIVITY HOURS")
            hour_data = filtered_df[filtered_df['peak_hour'] != -1] 
            if not hour_data.empty:
                hour_counts = hour_data['peak_hour'].value_counts().sort_index()
                st.line_chart(hour_counts, color="#39FF14") 
            else:
                st.info("Insufficient temporal data for this view.")
                
        st.markdown("<hr>", unsafe_allow_html=True)

        map_col, data_col = st.columns([2, 1])
        
        with data_col:
            st.subheader("DEPLOYMENT MANIFEST")
            
            target_options = ["OVERVIEW (ALL TARGETS)"] + [f"Rank {i+1}: {row['jurisdiction']} (Impact: {row['congestion_impact_score']})" for i, row in filtered_df.iterrows()]
            selected_target = st.selectbox("INITIATE TARGET LOCK:", target_options)
            
            st.markdown("<br>", unsafe_allow_html=True) 
            st.markdown("<h4 style='color: #00F0FF; border-bottom: 1px solid #39FF14; padding-bottom: 5px; font-family: monospace;'>ACTIONABLE STRIKE GRID</h4>", unsafe_allow_html=True)
            
            display_df = filtered_df[['jurisdiction', 'congestion_impact_score', 'peak_hour']].copy()
            display_df['peak_hour'] = display_df['peak_hour'].apply(lambda x: f"{int(x)}:00" if pd.notna(x) and x != -1 else "VAR")
            display_df.columns = ['JURISDICTION', 'IMPACT_SCORE', 'STRIKE_TIME'] 
            st.dataframe(display_df.sort_values('IMPACT_SCORE', ascending=False), use_container_width=True, hide_index=True)

        with map_col:
            st.subheader("TACTICAL DEPLOYMENT MAP")
            
            if selected_target == "OVERVIEW (ALL TARGETS)":
                map_center = [filtered_df['center_lat'].median(), filtered_df['center_lon'].median()]
                zoom_level = 12
            else:
                rank_idx = int(selected_target.split(':')[0].replace('Rank ', '')) - 1
                target_row = filtered_df.iloc[rank_idx]
                map_center = [target_row['center_lat'], target_row['center_lon']]
                zoom_level = 16 

            m = folium.Map(location=map_center, zoom_start=zoom_level, tiles='CartoDB dark_matter')

            
            if heat_data:
                HeatMap(heat_data, radius=12, blur=15, max_zoom=13, 
                        gradient={0.3: '#00008B', 0.5: '#00F0FF', 0.7: '#39FF14', 1.0: '#FF007F'}).add_to(m)

            
            for idx, row in filtered_df.iterrows():
                is_target = selected_target != "OVERVIEW (ALL TARGETS)" and idx == int(selected_target.split(':')[0].replace('Rank ', '')) - 1
                
                marker_radius = 15 if is_target else 8
                marker_opacity = 0.9 if is_target else 0.5
                
                peak_time = f"{int(row['peak_hour'])}:00 HRS" if pd.notna(row['peak_hour']) and row['peak_hour'] != -1 else "VARIABLE"
                popup_text = f"""
                <div style='width: 200px; font-family: monospace; color: #333;'>
                    <b>THREAT LEVEL:</b> {idx + 1}<br>
                    <b>STATION:</b> {row['jurisdiction']}<br>
                    <b>IMPACT SCORE:</b> <span style='color: red;'>{round(row['congestion_impact_score'], 1)}</span><br>
                    <b>JUNCTION PROXIMITY:</b> {row['junction_violations']} detected<br>
                    <b>OPTIMAL STRIKE TIME:</b> {peak_time}
                </div>
                """
                
                folium.CircleMarker(
                    location=[row['center_lat'], row['center_lon']],
                    radius=marker_radius,
                    color='#00F0FF',
                    weight=2,
                    fill=True,
                    fill_color='#FF007F',
                    fill_opacity=marker_opacity,
                    popup=folium.Popup(popup_text)
                ).add_to(m)

            st_folium(m, use_container_width=True, height=600)
    else:
        st.error("SYSTEM ERROR: No significant parking hotspots detected.")
else:
    st.title("NEURAL PARKING & CONGESTION GRID")
    st.info("SYSTEM STANDBY. AWAITING TELEMETRY UPLOAD IN SIDEBAR")
