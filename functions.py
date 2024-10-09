from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SHIFT

def cartesian_to_geo(x, y, min_lat, max_lat, min_lon, max_lon):
    lon = -(min_lon + ((min_lon - max_lon) * x / SCREEN_WIDTH))
    lat = max_lat - ((max_lat - min_lat) * y / SCREEN_HEIGHT)
    return lon, lat

def geo_to_cartesian(lon, lat, min_lat, max_lat, min_lon, max_lon):
    x = (min_lon - lon) * (SCREEN_WIDTH) / (min_lon - max_lon)
    y = (max_lat - lat) * (SCREEN_HEIGHT) / (max_lat - min_lat)
    return SHIFT + x, y 