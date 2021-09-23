import logging

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go

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

url = f"https://drive.google.com/uc?export=download&id=11AIX7aAqyG_tS5Khkrdm1H28pmH3ii_F"  # contains_kgiop_objects_4326
df_4326 = pd.read_json(url, orient="index")

url = f"https://drive.google.com/uc?export=download&id=18WfZTor3jqtGybrQEjGRFUZR6vMi0_sx"  # k_mean_points_distance
k_mean_points_distance_series = pd.read_json(url, orient="index")
k_mean_points_distance_series.rename(columns={0: "mean_distance"}, inplace=True)


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


def get_violin():
    data = [k_mean_points_distance_series[k_mean_points_distance_series["mean_distance"] < less] for less in
            [1000, 500, 250]]
    data.insert(0, k_mean_points_distance_series)

    names = ["all", "1000", "500", "250"]

    fig = go.Figure()
    for data_line, name in zip(data, names):
        fig.add_trace(go.Violin(x=data_line["mean_distance"], name=name))

    fig.update_traces(orientation="h", side="positive", width=3, points=False)
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False,
                      title="Среднее растояние до 5 ближайших объектов культурного наследия")
    fig.update_yaxes(type="category")

    return fig


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=get_density_streets_fig(df_roads)),
    dcc.Graph(figure=get_streets_with_points(gdf_kgiop_objects, df_roads)),
    dcc.Graph(figure=px.bar(df_4326, x=df_4326.index, y=0, log_y=True)),
    dcc.Graph(figure=get_violin()),
])


if __name__ == '__main__':
    app.run_server(debug=True)
