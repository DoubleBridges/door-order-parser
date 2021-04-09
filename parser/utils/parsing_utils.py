def get_formatted_text_from_line_obj(line_obj: object) -> str:
    return line_obj.get_text().replace("\n", "")


def get_start_and_end_ypos(item_list: list) -> list:

    current_idx = 0
    stop_idx = len(item_list) - 2

    while current_idx <= stop_idx:
        name_and_species = item_list[current_idx][0]
        name = name_and_species.split("(")[0].strip()
        species = (
            name_and_species.split(" ")[1].strip().replace(")", "").replace("(", "")
        )
        start_ypos = item_list[current_idx][1]
        end_ypos = item_list[current_idx + 1][1] + 20

        item_list[current_idx] = {
            "name": name,
            "start_y": start_ypos,
            "end_y": end_ypos,
            "species": species,
        }
        current_idx += 1

    item_list[-1] = {
        "name": item_list[-1][0].split("(")[0].strip(),
        "start_y": item_list[-1][1],
        "end_y": 0,
        "species": item_list[-1][0]
        .split("(")[1]
        .strip()
        .replace(")", "")
        .replace("(", ""),
    }

    return item_list


def sanitize_text(text_obj: object) -> str:
    return text_obj.get_text().strip().replace("\n", "")
