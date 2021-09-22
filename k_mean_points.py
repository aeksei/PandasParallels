from geopandas_dataframes import get_streets, get_kgiop_objects


if __name__ == "__main__":
    df_kgiop_objects = get_kgiop_objects()

    df_roads = get_streets()

    K_MEAN_POINTS = 5
    df_roads["mean_distance"] = df_roads.geometry.apply(
        lambda road: df_kgiop_objects.distance(road).nsmallest(K_MEAN_POINTS).mean())

    df_roads = df_roads.set_index("id")
    df_roads["mean_distance"].to_json("k_mean_points_distance.json")
