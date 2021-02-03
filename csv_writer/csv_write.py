import csv
from icecream import ic
from parser.quote_parser import QuoteDetails

data_dict = QuoteDetails("../sample_input.pdf")
ic(data_dict)