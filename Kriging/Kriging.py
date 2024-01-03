# Import modules
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pykrige.ok import OrdinaryKriging
import rasterio
import rasterio.mask
from rasterio.plot import show
from rasterio.transform import Affine
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import box
from shapely.geometry import Polygon, Point
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import geopandas as gpd
from shapely.geometry import Point

# Load data
philippines = gpd.read_file("Provinces.shp")
rainfall = pd.read_excel('output.xlsx')
# Load data

# Create a GeoDataFrame
geometry = [Point(lon, lat) for lon, lat in zip(rainfall['lon'], rainfall['lat'])]
gdf = gpd.GeoDataFrame(rainfall, geometry=geometry)
# Add the rainfall values to the GeoDataFrame
gdf['rainfall'] = rainfall['RR']

# Set the CRS to WGS 84 (EPSG:4326)
gdf.crs = 'EPSG:4326'
# Replace 'output_shapefile.shp' with your desired output shapefile name
gdf.to_file('output.shp')
rainfall = gpd.read_file('output.shp')
# Create a GeoDataFrame

# Reproject data 
proj = 'EPSG:4326'
philippines = philippines.to_crs(proj)
rainfall = rainfall.to_crs(proj)

# # Get X and Y coordinates of rainfall points
# x_rain = rainfall["geometry"].x
# y_rain = rainfall["geometry"].y

# # Create list of XY coordinate pairs
# coords_rain = [list(xy) for xy in zip(x_rain, y_rain)]

# # Get extent of counties feature
# min_x_philippines, min_y_philippines, max_x_philippines, max_y_philippines = philippines.total_bounds

# # Get list of rainfall "values"
# value_rain = list(rainfall["RR"])

# # Create a copy of counties dataset
# philippines_dissolved = philippines.copy()

# # Add a field with constant value of 1
# philippines_dissolved["constant"] = 1

# # Dissolve all counties to create one polygon
# philippines_dissolved = philippines_dissolved.dissolve(by = "constant").reset_index(drop = True)

# def export_kde_raster(Z, XX, YY, min_x, max_x, min_y, max_y, proj, filename):
#     '''Export and save a kernel density raster.'''

#     # Get resolution
#     xres = (max_x - min_x) / len(XX)
#     yres = (max_y - min_y) / len(YY)

#     # Set transform
#     transform = Affine.translation(min_x - xres / 2, min_y - yres / 2) * Affine.scale(xres, yres)

#     # Export array as raster
#     with rasterio.open(
#             filename,
#             mode = "w",
#             driver = "GTiff",
#             height = Z.shape[0],
#             width = Z.shape[1],
#             count = 1,
#             dtype = Z.dtype,
#             crs = proj,
#             transform = transform,
#     ) as new_dataset:
#             new_dataset.write(Z, 1)

# # Split data into testing and training sets
# coords_rain_train, coords_rain_test, value_rain_train, value_rain_test = train_test_split(coords_rain, value_rain, test_size = 0.20, random_state = 42)

# # Create separate GeoDataFrames for testing and training sets
# rain_train_gdf = gpd.GeoDataFrame(geometry = [Point(x, y) for x, y in coords_rain_train])
# rain_train_gdf["Actual_Value"] = value_rain_train
# rain_test_gdf = gpd.GeoDataFrame(geometry = [Point(x, y) for x, y in coords_rain_test])
# rain_test_gdf["Actual_Value"] = value_rain_test

# # Get minimum and maximum coordinate values of rainfall training points
# min_x_rain, min_y_rain, max_x_rain, max_y_rain = rain_train_gdf.total_bounds

# # Create subplots
# fig, ax = plt.subplots(1, 1, figsize = (10, 10))

# # Plot data
# philippines.plot(ax = ax, color = 'bisque', edgecolor = 'dimgray')
# rain_train_gdf.plot(ax = ax, marker = 'o', color = 'limegreen', markersize = 3)
# rain_test_gdf.plot(ax = ax, marker = 'o', color = 'royalblue', markersize = 3)






























