import streamlit as st
import osmnx as ox
import pandana
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import shapely

# Streamlit App
st.title("Street Network Analysis")

# User input for address
cityname = st.text_input("Enter Address:", '4602 West Franklin St, Richmond, VA')
crs = 4326

# Get graph by geocoding
graph = ox.graph_from_address(cityname, network_type="walk")

# Project graph
graph = ox.projection.project_graph(graph, to_crs=crs)

# Select points of interest based on osm tags
tags = {
    'amenity': [
        'cafe',
        'bar',
        'restaurant'
    ],
    'shop': [
        'bakery',
        'convenience',
        'supermarket',
        'department_store',
        'clothes',
        'shoes'
    ],
    'leisure': [
        'fitness_centre'
    ]
}

# Get amenities from place
pois = ox.geometries.geometries_from_address(cityname, tags=tags)
    
# Project pois
pois = pois.to_crs(epsg=crs)

# Max time to walk in minutes (no routing to nodes further than this)
walk_time = 15

# Walking speed
walk_speed = 7

# Set a uniform walking speed on every edge
for u, v, data in graph.edges(data=True):
    data['speed_kph'] = walk_speed
graph = ox.add_edge_travel_times(graph)

# Extract node/edge GeoDataFrames, retaining only necessary columns (for pandana)
nodes = ox.graph_to_gdfs(graph, edges=False)[['x', 'y']]
edges = ox.graph_to_gdfs(graph, nodes=False).reset_index()[['u', 'v', 'travel_time']]

# Construct the pandana network model
network = pandana.Network(
    node_x=nodes['x'],
    node_y=nodes['y'], 
    edge_from=edges['u'],
    edge_to=edges['v'],
    edge_weights=edges[['travel_time']]
)

# Extract centroids from the pois' geometries
centroids = pois.centroid

# Specify a max travel distance for analysis
# Minutes -> seconds
maxdist = walk_time * 60

# Set the pois' locations on the network
network.set_pois(
    category='pois',
    maxdist=maxdist,
    maxitems=1000,
    x_col=centroids.x, 
    y_col=centroids.y
)

# calculate travel time to 10 nearest pois from each node in network
distances = network.nearest_pois(
    distance=maxdist,
    category='pois',
    num_pois=10
)

# Set text parameters
COLOR = 'white'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR

# Setup plot
fig, ax = plt.subplots(figsize=(20,15))
ax.set_axis_off()
ax.set_aspect('equal')
fig.set_facecolor((0,0,0))

# Plot the street network
ox.plot_graph(graph, ax=ax, node_size=0, edge_linewidth=1, bgcolor='k', edge_color='gray', show=False, close=False)

# Plot distance to nearest POI
sc = ax.scatter(
    x=nodes['x'],
    y=nodes['y'], 
    c=distances[1],
    s=20,
    cmap='viridis_r',
)

# Label only the inputted street
target_street = cityname
for u, v, key, data in graph.edges(keys=True, data=True):
    if 'name' in data and target_street in data['name']:
        edge_geom = data['geometry']
        x, y = edge_geom.xy
        ax.text(x[len(x) // 2], y[len(y) // 2], data['name'], fontsize=10, color='white', ha='center')

# Colorbar
cb = fig.colorbar(sc, ax=ax, shrink=0.8, ticks=[0, 200, 400, 600, 800])
cb.ax.tick_params(color='none', labelsize=20)
cb.ax.set_yticklabels(['0', '4', '8', '12', '>= 16'])
cb.set_label('Walking time to nearest POI (minutes)', fontsize=20, fontweight='bold')

# Remove empty space
plt.tight_layout()

# Show plot in Streamlit
st.pyplot(fig)

st.success("Analysis completed!")
