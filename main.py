import sys

from parser.parser import JobDetails
from report_writer.report_writer import generate_order
from path_handler.path_handler import get_dest_path

try:
    job_name = sys.argv[1]
except IndexError:
    print("Must enter a job name in the form of 'Job Name'")

try:
    path = get_dest_path(sys.argv[1])
    job = JobDetails(f"{path}/PSReport.pdf")
except FileNotFoundError:
    print("No door report in job folder")

else:
    for style in job.door_styles:
        door_list = job.door_styles[style]["doors"]
        drawer_list = job.door_styles[style]["drawers"]

        generate_order(job, path, style, door_list, drawer_list)
        print(f"Generated {job.name}-{style}.pdf in Job Files/{job.name}/Door Orders")

sys.exit()