from parser.parser import JobDetails
from report_writer.report_writer import generate_order


job = JobDetails("sample_input/sample3.pdf")

for style in job.door_styles:
    door_list = job.door_styles[style]["doors"]
    drawer_list = job.door_styles[style]["drawers"]
    generate_order(job, style, door_list, drawer_list)
