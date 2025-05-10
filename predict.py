import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import base64

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
set_background("C:\\Users\\krish\\Downloads\\aimin8.jpg")

shapefile_path = "C:\\Users\\krish\\OneDrive\\Desktop\\python\\__pycache__\\calculator\\exploration_data_gis_view.shp"  # Replace with your actual file path
gdf = gpd.read_file(shapefile_path)
gdf['geographic'] = gdf['geographic'].apply(lambda val:1 if val=="DMS" else 0)

st.title("Predict")

X = gdf[['id', 'subid','row_number','geographic']].values  # Features - change this based on your shapefile columns

# Extract the label (target variable) - let's assume 'mineral_type' is the label
y = gdf['commodity'].values  # Target labels (e.g., 1 = gold, 0 = non-mineral)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=300, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
st.title("Accuracy:")
st.write(accuracy_score(y_test,y_pred))
# print("Classification Report:\n", classification_report(y_test, y_pred))
new_data1 = gdf[['id', 'subid','row_number','geographic']].values  
prediction = rf_model.predict(new_data1)
gdf['predicted_mineral_type'] = prediction

# Visualize the results on the map
gdf.plot(column='predicted_mineral_type', legend=False)
plt.title("Predicted Mineral Types")
st.pyplot(plt.gcf()) # instead of plt.show()
# Apply the trained model to the full dataset or new data points
# data1 = {'id':284,'subid':6729,'expid':67,'row_number':88,'geographic':1}
# new_data = gpd.GeoDataFrame(data=data1,index=[0])
new = {
    'id':st.number_input("Id",0,7359),
    'subid':st.number_input("Sub Id",0,12838),
    'row_number':st.number_input("Row Number",0,7635),
    'geographic':st.radio("Geographic(DD or DSM)",options=[0,1],index=None)
}
new_data = gpd.GeoDataFrame(data=new,index=[0])
predictions = rf_model.predict(new_data)
new_title = '<h1 style="font-family:sans-serif; color:White;-webkit-text-stroke: 1px black; font-size: 42px;">The Predicted Mineral is:</h1>'
st.markdown(new_title,unsafe_allow_html=True)
st.write(str(predictions))
