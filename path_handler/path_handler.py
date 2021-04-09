import os
from icecream import ic


def get_dest_path(job_path: str) -> str:
    os.chdir("/mnt/k")
    root_path = os.getcwd()
    path_to_job_list = job_path.split("/")

    def get_subfolders(path: str) -> list:
        return [f.name for f in os.scandir(path) if f.is_dir()]

    subfolders = get_subfolders(root_path)

    for folder in path_to_job_list:
        subfolders = get_subfolders(f"{root_path}/{folder}")
        root_path = f"{root_path}/{folder}"

    if "Door Orders" not in subfolders:

        print(
            """
        Door Orders folder does not exist in this job.
        Would you like to create one?
        """
        )

        response = input("Y/N\n")

        if response.lower() == "y":
            os.mkdir("Door Orders")
            os.chdir("Door Orders")
            path = os.getcwd()
        else:
            return FileNotFoundError

    else:
        ic(os.getcwd())
        os.chdir(f"{root_path}/Door Orders")
        path = os.getcwd()

    return path
