import action_generate_release_3d_printable
import action_generate_release_laser_cut


def main(**kwargs):
    action_generate_release_3d_printable.main(**kwargs)
    action_generate_release_laser_cut.main(**kwargs)
    pass    






if __name__ == "__main__":
    kwargs = {}

    main(**kwargs)
    pass