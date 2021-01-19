from parser.parser import JobDetails
from pprint import PrettyPrinter
from report_writer.report_writer import generate_order


job = JobDetails("sample_input/sample2.pdf")

pp = PrettyPrinter(indent=2)


pp.pprint(job.name)
# pp.pprint(job._text_lines)
# pp.pprint(job.order_date)
# pp.pprint(job.door_styles)
# pp.pprint((job.doors, job.drawers))

# for style in job.door_styles:
#     d_style = job.door_styles[style]
#     print(d_style)
#     generate_order(job, style, d_style["doors"])
