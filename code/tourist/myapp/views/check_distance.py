from myapp.models import *
from geopy.distance import geodesic
# ------------------------------------確定距離(傳place_id、座標)
def check_distance(get_user_address, a_id_list,ispet = False):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list , ispet=ispet):
        distance = geodesic(
            (get_user_address[0], get_user_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 2.5:
            ok_a_list.append([a.place_id, a.location_x, a.location_y])
    print(ok_a_list)
    return ok_a_list



# ------------------------------------確定距離(傳place_id)
def check_distance_placeid(get_user_address, a_id_list,ispet = False):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list,ispet=ispet):
        distance = geodesic(
            (get_user_address[0], get_user_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 2.5:
            ok_a_list.append(a.place_id)
    return ok_a_list

def check_distance_id(get_user_address, a_id_list,ispet = False):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list,ispet=ispet):
        distance = geodesic(
            (get_user_address[0], get_user_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 2.5:
            ok_a_list.append(a.id)
    return ok_a_list