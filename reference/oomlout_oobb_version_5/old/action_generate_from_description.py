import oobb
import oobb_base

def main(**kwargs):
    pass
    file_input = "things/oobb_bearing_plate_03_03_12_6704/3dpr.txt"
    file_output = "3dpr_test.scad"

    lines = ""
    #read in
    with open(file_input, 'r') as file:
        lines = file.readlines()

    objects = []
    for line in lines:
        objects.append(oobb_base.oobb_easy_string(item=line))

    oobb.opsc_make_object(file_output, objects, mode="3dpr", save_type="all", overwrite=True)



if __name__ == "__main__":
    main()
    pass