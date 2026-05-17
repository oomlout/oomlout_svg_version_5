import oobb_base
import copy

def get_common(**kwargs):
    shape = kwargs.get('s',kwargs.get('shape',""))
    #add get_ to shape and call the function named by that string
    print(f"get common shae: {shape}")

    kwargs["comment"] = f"{kwargs.get('comment','')}{kwargs.get('s','')}"
    kwargs.pop("s","")
    kwargs.pop("shape","")

    return eval(f"get_{shape}(**kwargs)")


def get_oobb_wire_clearance_square(**kwargs):
    depth = kwargs.get('t',kwargs.get('depth',10))
    pos = kwargs.get('pos',kwargs.get('p',[0,0,0]))

    pos_shift = [6.044,0,0]    
    size = [7, 10, depth]

    p3 = copy.deepcopy(kwargs)
    p3['t'] = "n"
    p3['s'] = "oobb_cube_center"
    pos = [pos[0] + pos_shift[0], pos[1] + pos_shift[1], pos[2] + pos_shift[2]]
    p3['pos'] = pos    
    p3['size'] = size

    return oobb_base.oe(**p3)