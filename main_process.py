import sys
from request_processor import RequestProcessor


# Base initialization code
file_path = sys.argv[1]
file_base_path, file_ext = ''.join(file_path.split('.')[:-1]), file_path.split('.')[-1]
write_file_basepath = file_base_path + '_output'
write_path = '.'.join([write_file_basepath, file_ext])
processor = RequestProcessor()
processor.read_requests(file_path)
processor.write_requests(write_path)