import sys

from parser.parser import JobDetails
from report_writer.report_writer import generate_order
from path_handler.path_handler import get_dest_path

job_name = sys.argv[1]

path = get_dest_path(sys.argv[1])
job = JobDetails(f"{path}/PSReport.pdf")

for style in job.door_styles:
    door_list = job.door_styles[style]["doors"]
    drawer_list = job.door_styles[style]["drawers"]

    generate_order(job, path, style, door_list, drawer_list)

sys.exit()