
import oomlout_ai_roboclick


def run_directory(directory, mode = "all", **kwargs):
    directory_path = directory
    working_yaml = f"{directory_path}\\working.yaml"
    
    run_kwargs = {
        "folder": directory_path,
        "file_action": working_yaml,
        "mode": mode,
    }
    run_kwargs.update(kwargs)
    oomlout_ai_roboclick.run_folder(**run_kwargs)



def main() -> int:
    directory = "C:\\od\\OneDrive\\docs\\helen_school_english_spelling_editing\\parts\\personal_helen_school_english_forced_editing_a_juggler_practicing_using_one_two_and_four_balls_to_juggle_topic_2025_12_29_date_49_count"
    run_directory(
        directory=directory,
        mode = "all"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
