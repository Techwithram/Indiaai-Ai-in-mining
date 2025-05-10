import streamlit as st
import geopandas as gpd
import folium
import colorsys
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import base64

def generate_interactive_map(shapefile_path, output_html_path="interactive_exploration_map.html", column_to_visualize=None):
    
    try:
        # --- 1. Load the Shapefile ---
        gdf = gpd.read_file(shapefile_path)

        if gdf.crs is None:
            print("Warning: CRS not found in shapefile. Assuming EPSG:4326.")
            gdf = gdf.set_crs("EPSG:4326", allow_override=True)
        elif gdf.crs.to_epsg() != 4326:
            print("Reprojecting to EPSG:4326 for Folium compatibility...")
            gdf = gdf.to_crs(epsg=4326)


        # --- 3. Create a Folium Map ---
        if not gdf.empty:
            gdf = gdf[gdf.geometry.is_valid]
            if not gdf.empty:
                centroid = gdf.geometry.unary_union.centroid
                map_center = [centroid.y, centroid.x]
                initial_zoom = 10 
            else:
                map_center = [0, 0]
                initial_zoom = 2
        else:
            map_center = [0, 0]
            initial_zoom = 2


        m = folium.Map(location=map_center, zoom_start=initial_zoom, tiles='OpenStreetMap') 


        # --- 4. Add GeoData to the Map ---
        def style_function(feature):
            # Default style
            return {
                'fillColor': '#3388ff',
                'color': '#3388ff',
                'weight': 2,
                'fillOpacity': 0.5
            }

        def highlight_function(feature):
             return {
                'fillColor': '#ffff00',
                'color': '#ffff00',
                'weight': 3,
                'fillOpacity': 0.7
            }

        # If a column for visualization is specified, use it for coloring
        if column_to_visualize and column_to_visualize in gdf.columns:
            # Handle potential non-string values in the visualization column
            gdf[column_to_visualize] = gdf[column_to_visualize].astype(str)

            # Get unique values from the column, dropping None/NaN and 'nan' string
            unique_values = gdf[column_to_visualize].dropna().unique()
            unique_values = [v for v in unique_values if v.lower() != 'nan']


            # Creating a color map using colorsys 
            num_colors = len(unique_values)
            # Generate colors with good separation
            colors = [f'#{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x}'
                      for c in [colorsys.hsv_to_rgb(i/max(1, num_colors), 0.8, 0.8) for i in range(num_colors)]]

            color_map = dict(zip(unique_values, colors))


            def color_style_function(feature):
                value = feature['properties'].get(column_to_visualize)
                # Handle potential None or non-string values gracefully
                value_str = str(value) if value is not None else 'nan'
                fill_color = color_map.get(value_str, '#808080') # Default to grey for missing/other
                return {
                    'fillColor': fill_color,
                    'color': '#000000', # Outline color
                    'weight': 1,
                    'fillOpacity': 0.7
                }

            style_func = color_style_function
        else:
            style_func = style_function


        # Add GeoJson layer to the map
        folium.GeoJson(
            gdf.to_json(), 
            style_function=style_func,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=list(gdf.columns.drop('geometry')), 
                aliases=[col.replace('_', ' ').title() for col in gdf.columns.drop('geometry')], 
                localize=True,
                sticky=False,
                labels=True,
                style="""
                    background-color: #F0EFEF;
                    border-radius: 3px;
                    box-shadow: 5px;
                """
            ),
            popup=folium.features.GeoJsonPopup(
                 fields=list(gdf.columns.drop('geometry')), 
                 aliases=[col.replace('_', ' ').title() for col in gdf.columns.drop('geometry')], 
                 localize=True,
                 labels=True,
                 style="background-color: #FFF; color: #333; font-family: arial; font-size: 12px; padding: 10px;"
            )
        ).add_to(m)

        folium.LayerControl().add_to(m)

        # --- 5. Output/Display the Map ---
        m.save(output_html_path)
        st_data = st_folium(m,width=1000)

    except FileNotFoundError:
        print(f"Error: Shapefile not found at {shapefile_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


if __name__ == "__main__":
    path_to_shapefile = st.text_input("Enter the path of the shapefile",placeholder="C:\\Users\\krish\\OneDrive\\Desktop\\python\\__pycache__\\calculator\\exploration_data_gis_view.shp")
    output_file = "my_exploration_interactive_map.html"
    set_background("C:\\Users\\krish\\Downloads\\aimin5.jpg")
    if st.toggle("Generate"):
        gdf = gpd.read_file(path_to_shapefile)
        col = gdf.columns
        min = gdf[['commodity']].drop_duplicates().values
        st.title("Available Minerals in this Shapefile")
        st.selectbox("Minerals",options=min)
        st.title("Generate Exploration Map")
        vis_col = st.selectbox("Select an aspect of creating the exploration map(column)",options=col)
        visualization_column = vis_col 

    
        generate_interactive_map(path_to_shapefile, output_file, column_to_visualize=visualization_column)

        st.title("Static Exploration Map")
        gdf.plot(column=vis_col,legend=False)
        st.pyplot(plt.gcf())