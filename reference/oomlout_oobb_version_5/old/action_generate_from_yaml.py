import oobb
import oobb_base
import yaml

def main(**kwargs):
    pass
    file_input = "things/oobb_bearing_plate_03_03_12_6704/3dpr.yaml"
    file_output = "3dpr_test.scad"

    objects_oobb = []    
    with open(file_input, 'r') as stream:
        try:
            objects_oobb = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    objects = []
    for object in objects_oobb:
        object_oobb = oobb_base.oobb_easy(**object)
        objects.extend(object_oobb)

    oobb.opsc_make_object(file_output, objects, mode="3dpr", save_type="all", overwrite=True)



if __name__ == "__main__":
    main()
    pass