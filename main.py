from parser.parser import JobDetails
from pprint import PrettyPrinter
from report_writer.report_writer import generate_order


job = JobDetails("sample_input/sample.pdf")

pp = PrettyPrinter(indent=2)


# pp.pprint(job.name)
# pp.pprint(job._text_lines)
# pp.pprint(job.order_date)
pp.pprint(job.door_styles)
# generate_order(job, "Slab-Birch", "Drawer Fronts")

print(job)