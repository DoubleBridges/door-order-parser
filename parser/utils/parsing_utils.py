def get_formatted_text_from_line_obj(line_obj) -> str:
    return line_obj.get_text().replace("\n", "")


def get_start_and_end_ypos(item_list: list) -> list:

    current_idx = 0
    stop_idx = len(item_list) - 2

    while current_idx <= stop_idx:
        name = item_list[current_idx][0]
        start_ypos = item_list[current_idx][1]
        end_ypos = item_list[current_idx + 1][1] + 20

        item_list[current_idx] = {
            "name": name,
            "start_y": start_ypos,
            "end_y": end_ypos,
        }
        current_idx += 1

    item_list[1] = {"name": item_list[-1][0], "start_y": item_list[-1][1], "end_y": 0}

    return item_list
