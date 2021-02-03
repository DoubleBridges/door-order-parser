import os


def get_dest_path(name: str) -> str:
    print(os.getcwd())
    os.chdir("/mnt/k")
    print(os.getcwd())
    path = os.getcwd()
    print(path)

    def get_subfolders(path: str) -> list:
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
