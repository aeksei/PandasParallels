import numpy as np
from shapely import geometry
import pandas as pd
import geopandas as gpd


def linestring_to_points(geo_df: gpd.GeoDataFrame) -> pd.DataFrame:
    lats = []
    lons = []
    names = []
    colors = []

    for feature, name, color in zip(geo_df.geometry, geo_df.id, geo_df.density_kgiop_objects):
        if isinstance(feature, geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            names = np.append(names, [name] * len(y))
            colors = np.append(colors, [color] * len(y))

            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            colors = np.append(colors, color)

    return pd.DataFrame({
        "lats": lats,
        "lons": lons,
        "names": names,
        "colors": colors,
    })