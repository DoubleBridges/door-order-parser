import os


def get_dest_path(job_path: str) -> str:
    os.chdir("/mnt/k")
    root_path = os.getcwd()
    path_to_job_list = job_path.split("/")

    def get_subfolders(path: str) -> list:
        return [f.name for f in os.scandir(path) if f.is_dir()]

    subfolders = get_subfolders(root_path)

    for folder in path_to_job_list:
        subfolders = get_subfolders(folder)

    if name not in subfolders:

        print(
            """
        Job folder does not exist.
        Would you like to create one and add a Door Orders directory?
        """
        )

        response = input("Y/N\n")

        if response.lower() == "y":
            order_path = f"{name}/Door Orders"
            os.mkdir(name)
            os.mkdir(order_path)
            os.chdir(order_path)
            path = os.getcwd()
        else:
            return FileNotFoundError

    else:
        os.chdir(f"{name}/Door Orders")
        path = os.getcwd()

    return path
