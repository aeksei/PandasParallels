import geopandas as gpd


if __name__ == "__main__":
    DRIVE_FILE_ID = "1kdqgi94qhdEVvOJAvlpHvurYcurh_5d9"
    url = f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}"

    df_kgiop_objects = gpd.read_file(url).iloc[:100]
    print(df_kgiop_objects.head())

    DRIVE_FILE_ID = "107DtdB8wUehAFoASn-rtQ1jokVam04FN"
    url = f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}"

    df_roads = gpd.read_file(url).iloc[:100]
    df_roads = df_roads.set_index("id")
    print(df_roads.head())

    K_MEAN_POINTS = 5
    mean_distance = df_roads.geometry.apply(
        lambda road: df_kgiop_objects.distance(road).nsmallest(K_MEAN_POINTS).mean())

    mean_distance.to_json("k_mean_points_distance.json")
