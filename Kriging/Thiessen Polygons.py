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

# Get X and Y coordinates of rainfall points
x_rain = rainfall["geometry"].x
y_rain = rainfall["geometry"].y

# Create list of XY coordinate pairs
coords_rain = [list(xy) for xy in zip(x_rain, y_rain)]

# Get extent of counties feature
min_x_philippines, min_y_philippines, max_x_philippines, max_y_philippines = philippines.total_bounds

# Get list of rainfall "values"
value_rain = list(rainfall["RR"])

# Create a copy of counties dataset
philippines_dissolved = philippines.copy()

# Add a field with constant value of 1
philippines_dissolved["constant"] = 1

# Dissolve all counties to create one polygon
philippines_dissolved = philippines_dissolved.dissolve(by = "constant").reset_index(drop = True)

def export_kde_raster(Z, XX, YY, min_x, max_x, min_y, max_y, proj, filename):
    '''Export and save a kernel density raster.'''

    # Get resolution
    xres = (max_x - min_x) / len(XX)
    yres = (max_y - min_y) / len(YY)

    # Set transform
    transform = Affine.translation(min_x - xres / 2, min_y - yres / 2) * Affine.scale(xres, yres)

    # Export array as raster
    with rasterio.open(
            filename,
            mode = "w",
            driver = "GTiff",
            height = Z.shape[0],
            width = Z.shape[1],
            count = 1,
            dtype = Z.dtype,
            crs = proj,
            transform = transform,
    ) as new_dataset:
            new_dataset.write(Z, 1)

# Split data into testing and training sets
coords_rain_train, coords_rain_test, value_rain_train, value_rain_test = train_test_split(coords_rain, value_rain, test_size = 0.20, random_state = 42)

# Create separate GeoDataFrames for testing and training sets
rain_train_gdf = gpd.GeoDataFrame(geometry = [Point(x, y) for x, y in coords_rain_train])
rain_train_gdf["Actual_Value"] = value_rain_train
rain_test_gdf = gpd.GeoDataFrame(geometry = [Point(x, y) for x, y in coords_rain_test])
rain_test_gdf["Actual_Value"] = value_rain_test

# Get minimum and maximum coordinate values of rainfall training points
min_x_rain, min_y_rain, max_x_rain, max_y_rain = rain_train_gdf.total_bounds

# Create subplots
fig, ax = plt.subplots(1, 1, figsize = (10, 10))

# Plot data
philippines.plot(ax = ax, color = 'white', edgecolor = 'black')
rain_train_gdf.plot(ax = ax, marker = 'o', color = 'green', markersize = 3)
rain_test_gdf.plot(ax = ax, marker = 'o', color = 'blue', markersize = 3)

# Remove axis and grid lines
ax.set_axis_off()
ax.grid(False)

# Extend extent of counties feature by using buffer
philippines_buffer = philippines.buffer(100000)

# Get extent of buffered input feature
min_x_cty_tp, min_y_cty_tp, max_x_cty_tp, max_y_cty_tp = philippines_buffer.total_bounds

# Use extent to create dummy points and add them to list of coordinates
coords_tp = coords_rain_train + [[min_x_cty_tp, min_y_cty_tp], [max_x_cty_tp, min_y_cty_tp],
                                 [max_x_cty_tp, max_y_cty_tp], [min_x_cty_tp, max_y_cty_tp]]

# Compute Voronoi diagram
tp = Voronoi(coords_tp)

# Create empty list of hold Voronoi polygons
tp_poly_list = []

# Create a polygon for each region
# 'regions' attribute provides a list of indices of the vertices (in the 'vertices' attribute) that make up the region
# Source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
for region in tp.regions:

    # Ignore region if -1 is in the list (based on documentation)
    if -1 in region:

        # Return to top of loop
        continue

    # Otherwise, pass
    else:
        pass

    # Check that region list has values in it
    if len(region) != 0:

        # Create a polygon by using the region list to call the correct elements in the 'vertices' attribute
        tp_poly_region = Polygon(list(tp.vertices[region]))

        # Append polygon to list
        tp_poly_list.append(tp_poly_region)

    # If no values, return to top of loop
    else:
        continue

# Create GeoDataFrame from list of polygon regions
tp_polys = gpd.GeoDataFrame(tp_poly_list, columns = ['geometry'])

# Clip polygon regions to the counties boundary
tp_polys_clipped = gpd.clip(tp_polys, philippines_dissolved)


























