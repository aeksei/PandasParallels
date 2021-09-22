import logging

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import geopandas as gpd

from utils import linestring_to_points


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

with open("kgiop_objects.geojson") as f:
    gdf_kgiop_objects = gpd.read_file(f)
with open("streets.geojson") as f:
    gdf_roads = gpd.read_file(f)

gdf_kgiop_objects = gdf_kgiop_objects.to_crs("EPSG:4326")

gdf_roads = gdf_roads.to_crs("EPSG:4326")
df_roads = linestring_to_points(gdf_roads)

gdf_roads.geometry = gdf_roads.geometry.buffer(0.0008).boundary
df_buffer = linestring_to_points(gdf_roads)


def get_density_streets_fig(df):
    fig = px.density_mapbox(df, lat="lats", lon="lons", z="colors",
                            color_continuous_scale=px.colors.sequential.Inferno,
                            hover_name="names", radius=5,
                            mapbox_style="carto-positron")

    return fig


def get_streets_with_points(gdf_point, df_linestring):
    colors = pd.cut(df_linestring["colors"], 10, px.colors.sequential.Inferno)
    fig = px.line_mapbox(df_linestring, lat="lats", lon="lons",
                         color=colors,
                         hover_name="names",
                         mapbox_style="carto-positron")

    fig.add_scattermapbox(
        lat=gdf_point.geometry.y,
        lon=gdf_point.geometry.x,
    )

    fig.add_scattermapbox(
        lat=df_buffer["lats"], lon=df_buffer["lons"],
        mode="markers+lines",
    )

    return fig


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=get_density_streets_fig(df_roads)),
    dcc.Graph(figure=get_streets_with_points(gdf_kgiop_objects, df_roads))
])


if __name__ == '__main__':
    app.run_server(debug=True)
