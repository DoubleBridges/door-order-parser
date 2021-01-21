import os


def get_dest_path(name: str) -> str:

    os.chdir("/mnt/j")
    path = os.getcwd()

    def get_subfolders(path):
        return [f.name for f in os.scandir(path) if f.is_dir()]

    subfolders = get_subfolders(path)

    if name not in subfolders:
        order_path = f"{name}/Door Orders"
        os.mkdir(name)
        os.mkdir(order_path)
        os.chdir(order_path)
        path = os.getcwd()
    else:
        os.chdir(f"{name}/Door Orders")
        path = os.getcwd()

    return path
