import logging

from pandarallel import pandarallel
import geopandas as gpd


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

pandarallel.initialize(progress_bar=True)

ROAD_BUFFER = 80  # meters


def get_kgiop_objects() -> gpd.GeoDataFrame:
    logger.info("Загрузка объектов культурного наследия.")
    DRIVE_FILE_ID = "1kdqgi94qhdEVvOJAvlpHvurYcurh_5d9"
    url = f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}"
    return gpd.read_file(url)


def get_streets() -> gpd.GeoDataFrame:
    logger.info("Загрузка улиц.")
    DRIVE_FILE_ID = "1bUT1E-QSbG1vpSNM2dOG2-LEVXSrPdo3"
    url = f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}"

    return gpd.read_file(url)


def density_kgiop_objects(df_roads, df_kgiop_objects, road_buffer):
    logger.info("Вычисление плотности объектов культурного наследия.")
    df_roads["contains_kgiop_objects"] = df_roads.geometry.parallel_apply(
        lambda road: sum(df_kgiop_objects["geometry"].within(road.buffer(road_buffer))))

    df_roads["density_kgiop_objects"] = df_roads["contains_kgiop_objects"] / df_roads.geometry.length


if __name__ == '__main__':
    df_kgiop_objects = get_kgiop_objects().iloc[:1000]
    df_roads = get_streets()[:1000]

    density_kgiop_objects(df_roads, df_kgiop_objects, ROAD_BUFFER)

    df_kgiop_objects.to_file("kgiop_objects.geojson", driver="GeoJSON")
    df_roads.to_file("streets.geojson", driver="GeoJSON")
