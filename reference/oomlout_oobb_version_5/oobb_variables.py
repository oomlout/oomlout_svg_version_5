import oobb

def initialize_variables():
    modes = ["laser", "true", "3dpr"]
    vl = {}
    # base variables
    oobb.set_variable("osp", 15)
    oobb.set_variable("osp_minus", 1)
    oobb.set_variable("osp_hole", "m6")
    oobb.set_variable("ospe", 15/2)
    oobb.set_variable("ospe_minus", 1/2)
    oobb.set_variable("ospe_hole", "m3")

    # bearing variables
    bearing_d = {}
    
    # experience
    #   15 prints as 15 id
    #   27 prints as 26.8 od  01 too big
    #   25.6 prints as 25.4 od 02 too small

    bearing_d["606"] = {"id":6, "id_e":0, "od":17, "od_e":0.075, "depth":6, "depth_e":0, "inner_holes":0}
    bearing_d["676"] = {"id":6, "id_e":0, "od":10, "od_e":0.05, "depth":3, "depth_e":0, "inner_holes":0}
    bearing_d["696"] = {"id":6, "id_e":0, "od":15, "od_e":0.05, "depth":5, "depth_e":0, "inner_holes":0}
    bearing_d["6701"] = {"id":12, "id_e":0, "od":18, "od_e":0.2, "depth":4, "depth_e":0, "inner_holes":1}
    bearing_d["6702"] = {"id":15, "id_e":0, "od":21, "od_e":0.2, "depth":4, "depth_e":0, "inner_holes":1}
    bearing_d["6703"] = {"id":17, "id_e":0, "od":23, "od_e":0.2, "depth":4, "depth_e":0, "inner_holes":1}
    bearing_d["6704"] = {"id":20, "id_e":0, "od":27, "od_e":0.2, "depth":4, "depth_e":-0.4, "inner_holes":1}
    bearing_d["6705"] = {"id":25, "id_e":0, "od":32, "od_e":0.15, "depth":4, "depth_e":-0.4, "inner_holes":1}
    bearing_d["6706"] = {"id":30, "id_e":0, "od":37, "od_e":0.2, "depth":4, "depth_e":0, "inner_holes":1}
    bearing_d["6707"] = {"id":35, "id_e":0, "od":44, "od_e":0.2, "depth":5, "depth_e":0, "inner_holes":1}
    bearing_d["6800"] = {"id":10, "id_e":0, "od":19, "od_e":0.2, "depth":5, "depth_e":0, "inner_holes":1}
    bearing_d["6801"] = {"id":12, "id_e":0, "od":21, "od_e":0.2, "depth":5, "depth_e":0, "inner_holes":1}
    bearing_d["6802"] = {"id":15, "id_e":0, "od":24, "od_e":0.2, "depth":5, "depth_e":0, "inner_holes":1}
    bearing_d["6803"] = {"id":17, "id_e":0, "od":26, "od_e":0.2, "depth":5, "depth_e":0, "inner_holes":1}
    bearing_d["6804"] = {"id":20, "id_e":0, "od":32, "od_e":0.2, "depth":7, "depth_e":0, "inner_holes":0}
    bearing_d["6805"] = {"id":25, "id_e":0, "od":37, "od_e":0.2, "depth":7, "depth_e":0, "inner_holes":0}
    bearing_d["6806"] = {"id":30, "id_e":0, "od":42, "od_e":0.2, "depth":7, "depth_e":0, "inner_holes":0}
    bearing_d["6807"] = {"id":35, "id_e":0, "od":47, "od_e":0.2, "depth":7, "depth_e":0, "inner_holes":3}
    bearing_d["6808"] = {"id":40, "id_e":0, "od":52, "od_e":0.2, "depth":7, "depth_e":0, "inner_holes":3}
    bearing_d["6809"] = {"id":45, "id_e":0, "od":58, "od_e":0.2, "depth":7, "depth_e":0, "inner_holes":3}
    bearing_d["6810"] = {"id":50, "id_e":0.1, "od":65, "od_e":0.2, "depth":7, "depth_e":-0.2, "inner_holes":3}
    bearing_d["6811"] = {"id":55, "id_e":0, "od":72, "od_e":0.2, "depth":9, "depth_e":0, "inner_holes":3}
    bearing_d["6812"] = {"id":60, "id_e":0, "od":78, "od_e":0.2, "depth":10, "depth_e":0, "inner_holes":4}
    bearing_d["6813"] = {"id":65, "id_e":0, "od":85, "od_e":0.2, "depth":10, "depth_e":0, "inner_holes":4}
    bearing_d["6814"] = {"id":70, "id_e":0, "od":90, "od_e":0.2, "depth":10, "depth_e":0, "inner_holes":4}
    bearing_d["6815"] = {"id":75, "id_e":0, "od":95, "od_e":0.2, "depth":10, "depth_e":0, "inner_holes":4}
    bearing_d["6816"] = {"id":80, "id_e":0, "od":100, "od_e":0.2, "depth":10, "depth_e":0, "inner_holes":5}
    bearing_d["6817"] = {"id":85, "id_e":0, "od":110, "od_e":0.2, "depth":13, "depth_e":0, "inner_holes":5}
    bearing_d["6818"] = {"id":90, "id_e":0, "od":115, "od_e":0.2, "depth":13, "depth_e":0, "inner_holes":5}
    bearing_d["6819"] = {"id":95, "id_e":0, "od":120, "od_e":0.2, "depth":13, "depth_e":0, "inner_holes":5}
    bearing_d["6820"] = {"id":100, "id_e":0, "od":125, "od_e":0.2, "depth":13, "depth_e":0, "inner_holes":0}
    bearing_d["6821"] = {"id":105, "id_e":0, "od":130, "od_e":0.2, "depth":13, "depth_e":0, "inner_holes":0}
    bearing_d["6822"] = {"id":110, "id_e":0, "od":140, "od_e":0.2, "depth":16, "depth_e":0, "inner_holes":0}
    bearing_d["6824"] = {"id":120, "id_e":0, "od":150, "od_e":0.2, "depth":16, "depth_e":0, "inner_holes":0}
    bearing_d["6826"] = {"id":130, "id_e":0, "od":165, "od_e":0.2, "depth":18, "depth_e":0, "inner_holes":0}
    bearing_d["6828"] = {"id":140, "id_e":0, "od":175, "od_e":0.2, "depth":18, "depth_e":0, "inner_holes":0}
    bearing_d["6830"] = {"id":150, "id_e":0, "od":190, "od_e":0.2, "depth":20, "depth_e":0, "inner_holes":0}


    for bn in bearing_d:
        vl[f'bearing_{bn}_id'] = [bearing_d[bn]["id"]/2, bearing_d[bn]["id"]/2, bearing_d[bn]["id"]/2 + bearing_d[bn]["id_e"]]
        vl[f'bearing_{bn}_od'] = [bearing_d[bn]["od"]/2, bearing_d[bn]["od"]/2, bearing_d[bn]["od"]/2 + bearing_d[bn]["od_e"]]
        vl[f'bearing_{bn}_depth'] = [bearing_d[bn]["depth"], bearing_d[bn]["depth"], bearing_d[bn]["depth"] + bearing_d[bn]["depth_e"]]
        vl[f'bearing_{bn}_inner_holes'] = [bearing_d[bn]["inner_holes"], bearing_d[bn]["inner_holes"], bearing_d[bn]["inner_holes"]]
        clear = 2
        if bn == "606":
            clear = 6
        vl[f'bearing_{bn}_clearance'] = [clear, clear, clear]
        vl[f'bearing_{bn}_id_catch'] = [vl[f'bearing_{bn}_id'][0]+clear/2, vl[f'bearing_{bn}_id'][1]+clear/2, vl[f'bearing_{bn}_id'][2]+clear/2]
        vl[f'bearing_{bn}_od_catch'] = [vl[f'bearing_{bn}_od'][0]-clear/2, vl[f'bearing_{bn}_od'][1]-clear/2, vl[f'bearing_{bn}_od'][2]-clear/2]
    
    ##### radiuses
    m = {}
    m["d5"] = 0.5
    m["d5_3dpr"] = 0.7
    m["d75"] = 0.75
    m["d75_3dpr"] = 0.95
    m["1"] = 1
    m["1_3dpr"] = 1.2
    m["1d4"] = 1.5
    m["1d4_3dpr"] = 2
    m["1d4_tight"] = 1.4
    m["1d5"] = 1.6
    m["1d5_3dpr"] = 1.8
    m["1_5"] = 1.6
    m["1_5_3dpr"] = 2
    m["1_6"] = 1.7
    m["1_6_3dpr"] = 2.2
    m["2"] = 2
    m["2_3dpr"] = 2.7
    m["2d5"] = 2.5
    m["2d5_3dpr"] = 3.1
    m["3"] = 3
    m["3_3dpr"] = 3.6
    m["3_screw_wood"] = 4
    m["3_screw_wood_3dpr"] = 4.25
    m["3d5"] = 3.5
    m["3d5_3dpr"] = 3.9
    m["3d5_screw_wood"] = 4.5
    m["3d5_screw_wood_3dpr"] = 4.75
    m["4"] = 4
    m["4_3dpr"] = 4.5
    m["4_screw_wood"] = 5.2
    m["4_screw_wood_3dpr"] = 5.75
    m["5"] = 5
    m["5_3dpr"] = 5.5
    m["5_screw_wood"] = 4.5
    m["5_screw_wood_3dpr"] = 5.5
    m["6"] = 6
    m["6_screw_wood"] = 4.5
    m["6_screw_wood_3dpr"] = 6.5
    m["6_3dpr"] = 6.5
    m["7"] = 7
    m["7_3dpr"] = 7.5
    m["8"] = 8
    m["8_3dpr"] = 8.5
    m["10"] = 10
    m["10_3dpr"] = 10.5
    m["11"] = 11
    m["11_3dpr"] = 12
    m["12"] = 12
    m["12_3dpr"] = 12.5

    ##### hole variables
    vl["hole_radius_md5"] = [m["d5"]/2, m["d5"]/2, m["d5_3dpr"]/2]
    vl["hole_radius_md75"] = [m["d75"]/2, m["d75"]/2, m["d75_3dpr"]/2]
    vl["hole_radius_m1"] = [m["1"]/2, m["1"]/2, m["1_3dpr"]/2]
    vl["hole_radius_m1_4"] = [m["1d4"]/2, m["1d4"]/2, m["1d4_3dpr"]/2]
    vl["hole_radius_m1_4_tight"] = [m["1d4_tight"]/2, m["1d4_tight"]/2, m["1d4_tight"]/2]
    vl["hole_radius_m1d5"] = [m["1d5"]/2, m["1d5"]/2, m["1d5_3dpr"]/2]
    vl["hole_radius_m1_5"] = [m["1d5"]/2, m["1d5"]/2, m["1d5_3dpr"]/2]
    vl["hole_radius_m1_6"] = [m["1_6"]/2, m["1_6"]/2, m["1_6_3dpr"]/2]
    vl["hole_radius_m2"] = [m["2"]/2, m["2"]/2, m["2_3dpr"]/2]
    vl["hole_radius_m2d5"] = [m["2d5"]/2, m["2d5"]/2, m["2d5_3dpr"]/2]
    vl["hole_radius_m2_5"] = [m["2d5"]/2, m["2d5"]/2, m["2d5_3dpr"]/2]
    vl["hole_radius_m3"] = [m["3"]/2, m["3"]/2, m["3_3dpr"]/2]
    vl["hole_radius_m3_screw_wood"] = [m["3_screw_wood"]/2, m["3_screw_wood"]/2, m["3_screw_wood_3dpr"]/2]
    vl["hole_radius_m3d5"] = [m["3d5"]/2, m["3d5"]/2, m["3d5_3dpr"]/2]
    vl["hole_radius_m3d5_screw_wood"] = [m["3d5_screw_wood"]/2, m["3d5_screw_wood"]/2, m["3d5_screw_wood_3dpr"]/2]
    vl["hole_radius_m3_5_screw_wood"] = [m["3d5_screw_wood"]/2, m["3d5_screw_wood"]/2, m["3d5_screw_wood_3dpr"]/2]
    vl["hole_radius_m3_5"] = [m["3d5"]/2, m["3d5"]/2, m["3d5_3dpr"]/2]
    vl["hole_radius_m3_sort"] = [m["3"]/2+0.5, m["3"]/2+0.5, m["3_3dpr"]/2+0.5]
    vl["hole_radius_m4"] = [m["4"]/2, m["4"]/2, m["4_3dpr"]/2]
    vl["hole_radius_m4_screw_wood"] = [m["4_screw_wood"]/2, m["4_screw_wood"]/2, m["4_screw_wood_3dpr"]/2]
    vl["hole_radius_m5"] = [m["5"]/2, m["5"]/2, m["5_3dpr"]/2]
    vl["hole_radius_m5_screw_wood"] = [m["5_screw_wood"]/2, m["5_screw_wood"]/2, m["5_screw_wood_3dpr"]/2]
    vl["hole_radius_m6"] = [m["6"]/2, m["6"]/2, m["6_3dpr"]/2]
    vl["hole_radius_m6_screw_wood"] = [m["6_screw_wood"]/2, m["6_screw_wood"]/2, m["6_screw_wood_3dpr"]/2]
    vl["hole_radius_m7"] = [m["7"]/2, m["7"]/2, m["7_3dpr"]/2]
    vl["hole_radius_m8"] = [m["8"]/2, m["8"]/2, m["8_3dpr"]/2]
    vl["hole_radius_m10"] = [m["10"]/2, m["10"]/2, m["10_3dpr"]/2]
    vl["hole_radius_m11"] = [m["11"]/2, m["11"]/2, m["11_3dpr"]/2]
    vl["hole_radius_m12"] = [m["12"]/2, m["12"]/2, m["12_3dpr"]/2]
    vl["hole_radius_little_m6"] = [m["6"]/2, m["6"]/2, m["6_3dpr"]/2-.4]



    # nut variables
    nuts = ["m1d5", "m3", "m6"]

    #normal nuts AND BOLTS
    vl["nut_radius_m1d5"] = [3.2*1.154/2, 3.2*1.154/2, 3.5 * 1.154/2]    
    vl["nut_depth_m1d5"] = [1.3, 1.3, 1.5]
    
    vl["nut_radius_m1_5"] = [3.2*1.154/2, 3.2*1.154/2, 3.5 * 1.154/2]    
    vl["nut_depth_m1_5"] = [1.3, 1.3, 1.5]

    vl["nut_radius_m1_6"] = [3.2*1.154/2, 3.2*1.154/2, 3.5 * 1.154/2]    
    vl["nut_depth_m1_6"] = [1.3, 1.3, 1.5]


    vl["nut_radius_m2"] = [4*1.154/2, 4*1.154/2, 4.2 * 1.154/2]
    vl["nut_depth_m2"] = [1.6, 1.6, 1.8]    

    vl["nut_radius_m2d5"] = [5*1.154/2, 5*1.154/2, 5.4 * 1.154/2]
    vl["nut_depth_m2d5"] = [1.9, 1.9, 2.1]
    vl["nut_radius_m2_5"] = vl["nut_radius_m2d5"]
    vl["nut_depth_m2_5"] = vl["nut_depth_m2d5"]

    vl["nut_radius_m3"] = [5.5*1.154/2, 5.5*1.154/2, 6 * 1.154/2]
    vl["standoff_radius_m3"] = [5.8*1.154/2, 5.8*1.154/2, 6.3 * 1.154/2]
    #style 01
    vl["threaded_insert_01_radius_m3"] = [3.8/2, 4.2/2, 4.2/2]
    vl["threaded_insert_01_depth_m3"] = [6, 6, 6]
    vl["nut_depth_m3"] = [2.5, 2.5, 3]
    vl["threaded_insert_01_insertion_cone_m3"] = [0, 0, 0.5]


    vl["nut_radius_m4"] = [7*1.154/2, 7*1.154/2, 7.4 * 1.154/2]
    vl["nut_depth_m4"] = [3.2, 3.2, 3.5]

    vl["nut_radius_m5"] = [8*1.154/2, 8*1.154/2, 8.4 * 1.154/2]
    vl["bolt_radius_m5"] = vl["nut_radius_m5"]
    vl["bolt_depth_m5"] = [3.5, 3.5, 3.6]
    vl["nut_depth_m5"] = [4, 4, 4.5]

    vl["nut_radius_m6"] = [10*1.154/2, 10*1.154/2, 10.25 * 1.154/2]
    vl["bolt_radius_m6"] = vl["nut_radius_m6"]
    vl["bolt_depth_m6"] = [4, 4, 4.5]
    vl["nut_depth_m6"] = [5, 5, 5.5]

    vl["nut_radius_m8"] = [13*1.154/2, 13*1.154/2, 13.5 * 1.154/2]
    vl["bolt_radius_m8"] = vl["nut_radius_m8"]
    vl["bolt_depth_m8"] = [5.3, 5.3, 5.4]
    vl["nut_depth_m8"] = [6.5, 6.5, 6.8]

    vl["nut_radius_m10"] = [17*1.154/2, 17*1.154/2, 17.5 * 1.154/2]
    vl["bolt_radius_m10"] = vl["nut_radius_m10"]
    vl["bolt_depth_m10"] = [6.4, 6.4, 6.5]
    vl["nut_depth_m10"] = [10, 10, 10.5]

    vl["nut_radius_m12"] = [19*1.154/2, 19*1.154/2, 19.6 * 1.154/2]
    vl["bolt_radius_m12"] = vl["nut_radius_m12"]
    vl["bolt_depth_m12"] = [7.5, 7.5, 7.6]
    vl["nut_depth_m12"] = [10, 10, 10.5]


    #loose nuts
    m1d5_extra_radius = 0.2
    m1d5_extra_depth = 0.1
    vl["nut_radius_loose_m1d5"] = [vl["nut_radius_m1d5"][0] + m1d5_extra_radius, vl["nut_radius_m1d5"][1] + m1d5_extra_radius, vl["nut_radius_m1d5"][2] + m1d5_extra_radius]
    vl["nut_depth_loose_m1d5"] = [vl["nut_depth_m1d5"][0] + m1d5_extra_depth, vl["nut_depth_m1d5"][1] + m1d5_extra_depth, vl["nut_depth_m1d5"][2] + m1d5_extra_depth]
    
    vl["nut_radius_loose_m1_5"] = [vl["nut_radius_m1d5"][0] + m1d5_extra_radius, vl["nut_radius_m1d5"][1] + m1d5_extra_radius, vl["nut_radius_m1d5"][2] + m1d5_extra_radius]
    vl["nut_depth_loose_m1_5"] = [vl["nut_depth_m1d5"][0] + m1d5_extra_depth, vl["nut_depth_m1d5"][1] + m1d5_extra_depth, vl["nut_depth_m1d5"][2] + m1d5_extra_depth]
    
    vl["nut_radius_loose_m1_6"] = [vl["nut_radius_m1d5"][0] + m1d5_extra_radius, vl["nut_radius_m1d5"][1] + m1d5_extra_radius, vl["nut_radius_m1d5"][2] + m1d5_extra_radius]
    vl["nut_depth_loose_m1_6"] = [vl["nut_depth_m1d5"][0] + m1d5_extra_depth, vl["nut_depth_m1d5"][1] + m1d5_extra_depth, vl["nut_depth_m1d5"][2] + m1d5_extra_depth]
    

    m3_extra_radius = 0.1
    m3_extra_depth = 0.1
    vl["nut_radius_loose_m3"] = [vl["nut_radius_m3"][0] + m3_extra_radius, vl["nut_radius_m3"][1] + m3_extra_radius, vl["nut_radius_m3"][2] + m3_extra_radius]    
    vl["nut_depth_loose_m3"] = [vl["nut_depth_m3"][0] + m3_extra_depth, vl["nut_depth_m3"][1] + m3_extra_depth, vl["nut_depth_m3"][2] + m3_extra_depth]

    m6_extra_radius = 0.4
    m6_extra_depth = 0.4
    vl["nut_radius_loose_m6"] = [vl["nut_radius_m6"][0] + m6_extra_radius, vl["nut_radius_m6"][1] + m6_extra_radius, vl["nut_radius_m6"][2] + m6_extra_radius]
    vl["nut_depth_loose_m6"] = [vl["nut_depth_m6"][0] + m6_extra_depth, vl["nut_depth_m6"][1] + m6_extra_depth, vl["nut_depth_m6"][2] + m6_extra_depth]
    

    tight = -0.4
    for nut in nuts:
        vl["nut_width_" + nut] = [vl[f'nut_radius_{nut}'][0] * 2, vl[f'nut_radius_{nut}'][1] * 2, vl[f'nut_radius_{nut}'][2] * 2]
        vl[f"nut_radius_{nut}_tight"] = [vl[f'nut_radius_{nut}'][0] + tight, vl[f'nut_radius_{nut}'][1] +tight, vl[f'nut_radius_{nut}'][2] +tight]
        vl["nut_height_" + nut] = [vl[f'nut_depth_{nut}'][0] * 2 / 1.154, vl[f'nut_depth_{nut}'][1] * 2  / 1.154, vl[f'nut_depth_{nut}'][2] * 2  / 1.154]

    ###### o rings
    """
    oring_d = {}
    id_e_default = 4
    oring_d["327"] = {"id":43.82, "id_e":id_e_default, "od":54.48, "od_e":0.2, "depth":5.33, "depth_e":0, "inner_holes":3}
    oring_d["333"] = {"id":62.87, "id_e":id_e_default, "od":73.53, "od_e":0.2, "depth":5.33, "depth_e":0, "inner_holes":2}
    """
    directory_oring = "data/oring"
    #loat oring data from directory
    try:
        oring_data = read_csv_files(directory_oring)
        oring_d = {}
        id_e_default = 4
        for oring in oring_data:
            try:
                oring_name = oring["Size"]
                id = float(oring.get("I.D. MM", oring.get("I.D.", 0.0)))
                od = float(oring.get("O.D. MM", oring.get("O.D.", 0.0)))
                id_e_default = int(id / 10)
                depth = float(oring.get("C.S. MM", oring.get("C.S.", 0.0)))
                oring_d[oring_name] = {"id":id, "id_e":id_e_default, "od":od, "od_e":0.2, "depth":depth, "depth_e":0, "inner_holes":0}
            except:
                print(f"error reading oring data {oring_name}")
    




        for bn in oring_d:
            vl[f'oring_{bn}_id'] = [oring_d[bn]["id"]/2, oring_d[bn]["id"]/2, oring_d[bn]["id"]/2]
            vl[f'oring_{bn}_id_tight'] = [oring_d[bn]["id"]/2 + oring_d[bn]["id_e"], oring_d[bn]["id"]/2 + oring_d[bn]["id_e"], oring_d[bn]["id"]/2 + oring_d[bn]["id_e"]]
            vl[f'oring_{bn}_od'] = [oring_d[bn]["od"]/2, oring_d[bn]["od"]/2, oring_d[bn]["od"]/2 + oring_d[bn]["od_e"]]
            vl[f'oring_{bn}_depth'] = [oring_d[bn]["depth"], oring_d[bn]["depth"], oring_d[bn]["depth"]]
            vl[f'oring_{bn}_inner_holes'] = [oring_d[bn]["inner_holes"], oring_d[bn]["inner_holes"], oring_d[bn]["inner_holes"]]
    
    except:
            pass

    # screw variables
    screws = ["m1d5", "m3", "m6"]

    vl["screw_radius_m1d5"] = m["1d5"]/2, m["1d5"]/2, m["1d5_3dpr"]/2
    vl["screw_countersunk_radius_m1d5"] = [2.35/2, 2.5/2, 3/2]    
    vl["screw_countersunk_height_m1d5"] = [1/2, 1/2, 2/2]
    vl["screw_countersunk_depth_m1d5"] = vl["screw_countersunk_height_m1d5"]

    vl["screw_radius_m1_5"] = m["1_5"]/2, m["1_5"]/2, m["1_5_3dpr"]/2
    vl["screw_countersunk_radius_m1_5"] = [2.35/2, 2.5/2, 3/2]    
    vl["screw_countersunk_height_m1_5"] = [1/2, 1/2, 2/2]
    vl["screw_countersunk_depth_m1_5"] = vl["screw_countersunk_height_m1_5"]

    vl["screw_radius_m1_6"] = m["1_6"]/2, m["1_6"]/2, m["1_6_3dpr"]/2
    vl["screw_countersunk_radius_m1_6"] = [2.75/2, 2.8/2, 3.5/2]    
    vl["screw_countersunk_height_m1_6"] = [1/2, 1/2, 2.4/2]
    vl["screw_countersunk_depth_m1_6"] = vl["screw_countersunk_height_m1_6"]


    vl["screw_radius_m2"] = m["2"]/2, m["2"]/2, m["2_3dpr"]/2
     
    vl["screw_self_tapping_hole_radius_m2"] = [1.5/2, 1.5/2, 2.0/2]
    vl["screw_self_tapping_hole_loose_radius_m2"] = [2/2, 2/2, 2.75/2]
    vl["screw_self_tapping_washer_radius_m2"] = [5/2, 5/2, 5.5/2]    
    vl["screw_self_tapping_radius_m2"] = vl["screw_self_tapping_washer_radius_m2"]
    vl["screw_self_tapping_height_m2"] = [1.25, 1.3, 2.5]
    vl["screw_self_tapping_depth_m2"] = vl["screw_self_tapping_height_m2"]

    vl["screw_countersunk_radius_m2"] = [3.6/2, 4/2, 6/2]    #added 1.8 to m3 so trying adding 1.8 here
    vl["screw_countersunk_height_m2"] = [1.3/2, 1.3/2, 1.7/2]
    vl["screw_countersunk_depth_m2"] = vl["screw_countersunk_height_m2"]



    vl["screw_radius_m2d5"] = m["2d5"]/2, m["2d5"]/2, m["2d5_3dpr"]/2
    vl["screw_countersunk_radius_m2d5"] = [3.1/2, 4.5/2, 6.9/2]    #added 1.8 to m3 so trying adding 1.8 here
    vl["screw_countersunk_height_m2d5"] = [1.5/2, 1.5/2, 2/2]
    vl["screw_countersunk_depth_m2d5"] = vl["screw_countersunk_height_m2d5"]
    vl["screw_countersunk_radius_m2_5"] = vl["screw_countersunk_radius_m2d5"]
    vl["screw_countersunk_height_m2_5"] = vl["screw_countersunk_height_m2d5"]
    vl["screw_countersunk_depth_m2_5"] = vl["screw_countersunk_height_m2d5"]

    vl["screw_radius_m3"] = m["3"]/2, m["3"]/2, m["3_3dpr"]/2
    vl["screw_countersunk_radius_m3"] = [4.8/2, 5.8/2, 7.2/2]
    vl["screw_countersunk_height_m3"] = [1.7, 1.7, 1.9]
    vl["screw_countersunk_depth_m3"] = vl["screw_countersunk_height_m3"]
    vl["screw_socket_cap_radius_m3"] = [5.8/2, 5.8/2, 6/2]
    vl["screw_socket_cap_height_m3"] = [3, 3, 3.2]
    
    vl["screw_radius_m3_screw_wood"] = m["3"]/2, m["3"]/2, m["3_3dpr"]/2
    vl["screw_countersunk_radius_m3_screw_wood"] = [7/2, 7/2, 7.5/2]
    vl["screw_countersunk_height_m3_screw_wood"] = [2.5, 2.5, 3]
    vl["screw_countersunk_depth_m3_screw_wood"] = vl["screw_countersunk_height_m3_screw_wood"]
    
    vl["screw_radius_m3d5_screw_wood"] = m["3d5"]/2, m["3d5"]/2, m["3d5_3dpr"]/2
    vl["screw_countersunk_radius_m3d5_screw_wood"] = [7.8/2, 7.8/2, 9/2]
    vl["screw_countersunk_height_m3d5_screw_wood"] = [4, 4, 4.2]
    vl["screw_countersunk_depth_m3d5_screw_wood"] = vl["screw_countersunk_height_m3d5_screw_wood"]

    vl["screw_radius_m3_5_screw_wood"] = m["3d5"]/2, m["3d5"]/2, m["3d5_3dpr"]/2
    vl["screw_countersunk_radius_m3_5_screw_wood"] = [7.8/2, 7.8/2, 9/2]
    vl["screw_countersunk_height_m3_5_screw_wood"] = [4, 4, 4.2]
    vl["screw_countersunk_depth_m3_5_screw_wood"] = vl["screw_countersunk_height_m3d5_screw_wood"]



    vl["screw_radius_m4_screw_wood"] = m["4"]/2, m["4"]/2, m["4_3dpr"]/2
    vl["screw_countersunk_radius_m4_screw_wood"] = [9.8/2, 10.8/2, 10.8/2]
    vl["screw_countersunk_height_m4_screw_wood"] = [3.7, 3.7, 3.9]
    vl["screw_countersunk_depth_m4_screw_wood"] = vl["screw_countersunk_height_m4_screw_wood"]
    
    vl["screw_radius_m5_screw_wood"] = [m["5"]/2, m["5"]/2, m["5_3dpr"]/2]
    vl["screw_countersunk_radius_m5_screw_wood"] = [9.75/2, 9.75/2, 11/2]
    vl["screw_countersunk_height_m5_screw_wood"] = [3.75, 3.75, 4.2]
    vl["screw_countersunk_depth_m5_screw_wood"] = vl["screw_countersunk_height_m5_screw_wood"]

    vl["screw_radius_m6_screw_wood"] = [m["6"]/2, m["6"]/2, m["6_3dpr"]/2]
    vl["screw_countersunk_radius_m6_screw_wood"] = [11.5/2, 11.55/2, 13/2]
    vl["screw_countersunk_height_m6_screw_wood"] = [5, 5, 6]
    vl["screw_countersunk_depth_m6_screw_wood"] = vl["screw_countersunk_height_m6_screw_wood"]

    #larger for a screw sort jig
    ex = 0.5
    vl["screw_radius_m3_sort"] = m["3"]/2+ex, m["3"]/2+ex, m["3_3dpr"]/2+ex
    vl["screw_countersunk_radius_m3_sort"] = [4.8/2+ex, 5.8/2+ex, 7.2/2+ex]
    vl["screw_countersunk_height_m3_sort"] = [1.7+ex, 1.7+ex, 1.9+ex]
    vl["screw_countersunk_depth_m3_sort"] = vl["screw_countersunk_height_m3_sort"]

    vl["screw_self_tapping_hole_radius_m3"] = [2.5/2, 2.5/2, 3/2]
    vl["screw_self_tapping_hole_loose_radius_m3"] = [3/2, 3/2, 3.5/2]
    vl["screw_self_tapping_washer_radius_m3"] = [6/2, 6/2, 6.4/2]    
    vl["screw_self_tapping_radius_m3"] = vl["screw_self_tapping_washer_radius_m3"]
    vl["screw_self_tapping_height_m3"] = [1.5, 1.5, 2]
    vl["screw_self_tapping_depth_m3"] = vl["screw_self_tapping_height_m3"]

    current = 2.3
    vl["screw_self_tapping_hole_radius_m2_3"] = [current-0.5/2, current-0.5/2, current/2]
    vl["screw_self_tapping_hole_loose_radius_m2_3"] = [current/2, current/2, (current+0.5)/2]
    vl["screw_self_tapping_washer_radius_m2_3"] = [(current*2)/2, (current*2)/2,    (current*2+0.4)/2]        
    vl["screw_self_tapping_radius_m2_3"] = [3.7/2, 3.7/2,    (3.7+0.4)/2]
    vl["screw_self_tapping_height_m2_3"] = [1, 1, 1.5]
    vl["screw_self_tapping_depth_m2_3"] = vl["screw_self_tapping_height_m2_3"]


    vl["screw_radius_m6"] = m["6"]/2, m["6"]/2, m["6_3dpr"]/2
    vl["screw_countersunk_radius_m6"] = [6/2, 6/2, 7.2/2]
    vl["screw_countersunk_height_m6"] = [3.3, 3.3, 3.7]
    vl["screw_countersunk_depth_m6"] = vl["screw_countersunk_height_m6"]
    vl["screw_socket_cap_radius_m6"] = [10/2, 10/2, 11/2]
    vl["screw_socket_cap_height_m6"] = [6, 6, 6.2]

    ##### wire variables
    wi_extra = 0.3
    vl["wi_extra"] = [0,0,wi_extra]
    vl["wi_depth"] = [3, 2.54, 2.54+wi_extra]
    vl["wi_i01"] = [2.54, 2.54, 2.54]
    vl["wi_length"] = [14,14,14+wi_extra]

    for screw in screws:
        vl["screw__countersunk_height_" + screw] = [vl[f'screw_countersunk_radius_{screw}'][0] * 2, vl[f'screw_countersunk_radius_{screw}'][1] * 2, vl[f'screw_countersunk_radius_{screw}'][2] * 2]
        vl["screw__countersunk_width_" + screw] = [vl[f'screw_countersunk_height_{screw}'][0], vl[f'screw_countersunk_height_{screw}'][1], vl[f'screw_countersunk_height_{screw}'][2]]


    # zip tie
    vl["ziptie_height"] = [1.5, 1, 1.5]
    vl["ziptie_width"] = [4, 3, 4]

    # electronics
    ex = 0.2
    vl["i2d54"] = [2.54, 2.54, 2.54+ex]
    #lengths of i2d54
    for x in range(1,50):
        vl[f"i2d54x{x}"] = [2.54*x, 2.54*x, (2.54*x)+ex]
    vl["electronics_socket_i2d54_depth"] = [8.5, 8.5, 8.5+ex]

    for var in vl:
        values = vl[var]
        for i in range(0, len(modes)):
            oobb.set_variable(var, values[i], modes[i])





import os
import csv

oobb_directory_abs = r'C:\GH\oomlout_oobb_v3'

def read_csv_files(directory):
    data_dict = []
    #test if directory exists
    if not os.path.isdir(directory):
        print("directory does not exist")
        #add directory abs to it
        directory = os.path.join(oobb_directory_abs, directory)
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data_dict.append(row)
                #data_dict[filename] = rows
    return data_dict