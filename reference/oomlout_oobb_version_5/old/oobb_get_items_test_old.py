import copy
from oobb_get_items_base import *
import oobb_base as ob

## no longer used
def get_test_nut(size, depth=4.5, test="radius", difference=0.1, loose=False, **kwargs):
    shape = f"oobb_nut"
    radius_name = size
    name_variable = f"nut_{test}_{size}"
    switch_portion = test
    
    wid = 3
    hei = 3
    return get_test(name_variable, switch_portion, difference, wid, hei, radius_name=radius_name, depth=depth, shape=shape, loose=loose, **kwargs)


def get_test_old_1(**kwargs):
    radius = True
    wid = 3
    hei = 3
    padding = kwargs.get("padding", 7)
    zz = kwargs.get("z", 0)
    name_variable = kwargs["name"]
    radius_name = kwargs["radius_name"]
    difference = kwargs["difference"]
    depth_adjust = kwargs.get("depth_adjust", 0)
    if radius:
        name_variable_full = f'{name_variable}_{radius_name}'
        radius_mm = ob.gv(f'{name_variable_full}', "true")
        wid_mm = radius_mm
        hei_mm = radius_mm
        wid_tot_mm = (radius_mm + padding) * wid
        hei_tot_mm = (radius_mm + padding) * hei

    # switch to making it a test for variable take variable and shape
    # add tight and loose tolerances
    depth = kwargs.get("depth", 3)
    depth_item = depth + depth_adjust

    shape = kwargs["shape"]

    thing = ob.get_default_thing(**kwargs)

    # thing.update({"description": f"test {shape} with variable {name_variable}  portion {switch_portion} difference {difference}"})

    thing.update({"components": []})

    # base shape
    thing["components"].append(ob.oobb_easy(
        type="positive", shape="rounded_rectangle", size=[wid_tot_mm, hei_tot_mm, depth]))

    # get rid of size
    kwargs.pop("size", None)

    total_iterations = 0

    start_x = -wid_tot_mm/2 + (wid_mm+padding)/2
    start_y = -hei_tot_mm/2 + (hei_mm+padding)/2
    sizes = ""
    for w in range(wid):
        for h in range(hei):
            x = start_x + w * (wid_mm + padding)
            y = start_y + h * (hei_mm + padding)
            z = depth_item + zz
            total_iterations += 1
            kwargs["pos"] = [x, y, z]
            kwargs["name_variable_full"] = name_variable_full
            dif = (((wid * hei)+1)/2 * -difference) + \
                (total_iterations) * difference

            kwargs["difference"] = dif

            # kwargs["m"] = "#"
            p2 = copy.deepcopy(kwargs)
            depth2 = p2.get("depth2", None)
            if depth2 != None:
                #shift pos z down depth2
                p2["pos"][2] -= depth2

            p2.update({"depth": depth2})
            p2.update({"m": "#"})
            rv = get_test_item(**p2)
            sizes += f"total_itterations: {total_iterations} size: {rv[1]}\n"
            thing["components"].extend(rv[0])
            #insert holes for marking 0 point and direction
            if total_iterations == 1 or total_iterations == 2:
                p2 = copy.deepcopy(kwargs)
                #set pos z to 0
                p2["pos"][2] = -125
                p2.pop("depth")
                p2["shape"] = "oobb_hole"
                p2["radius_name"] = "m1d5"
                p2["type"] = "n"
                #p2["m"]= "#"
                thing["components"].extend(ob.oobb_easy(**p2))

    thing.update(
        {"description": f"test {shape} with variable {name_variable}  difference {difference} \n sizes \n{sizes}"})

    return thing


def get_test_item(**kwargs):
    name_variable_full = kwargs["name_variable_full"]
    difference = kwargs["difference"]
    new_value = []
    kwargs["type"] = "negative"
    modes = ["laser", "true", "3dpr"]
    orig_value = {}
    for mode in modes:
        orig_value[mode] = ob.gv(name_variable_full, mode)
        nv = orig_value[mode] + difference
        ob.set_variable(name_variable_full, nv, mode)
        new_value.append(nv)
    kwargs["m"] = ""
    obj = ob.oobb_easy(**kwargs)
    for mode in modes:
        ob.set_variable(name_variable_full, orig_value[mode], mode)

    return obj, new_value
