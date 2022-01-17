import os

from exceptions import WrongRequestException
from movie_seat_allocator import MovieSeatAllocator


class RequestProcessor:
    """
    Processes the input file of requests
    """
    def __init__(self):
        self.allocated_seats = []

    def read_requests(self, file_path):
        """
        Parse the file and allocate seats for each request
        :param file_path: File path to be read
        :return: None
        """
        allocator = MovieSeatAllocator()
        with open(file_path, 'r') as file:
            for line in file:
                request_id, num_seats = self.parse_request(line)
                self.allocated_seats.append(allocator.allocate_seats(request_id, num_seats))
        final_layout = allocator.theatre_layout
        for row_name, seats in final_layout.items():
            print(f'{row_name}  {" ".join(list(map(str, seats)))}')
        print("\n      ---------MOVIE SCREEN---------")
        file.close()

    def write_requests(self, file_path):
        """
        Returns the new file with
        :param file_path:
        :return: File Path where final allocations are mentioned
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except PermissionError as e:
            print("Not enough permissions to delete older file")
            return
        with open(file_path, 'w') as file:
            for row in self.allocated_seats:
                file.write(row + '\n')
        file.close()
        print(file_path)

    @staticmethod
    def parse_request(request):
        try:
            request_id = request.split(" ")[0]
            num_seats = int(request.split(" ")[1])
            if request_id is None or request_id == "" or len(request.split(" ")) > 2:
                raise WrongRequestException("Request not in proper format")
            return request_id, num_seats
        except Exception as e:
            raise WrongRequestException("Request not in proper format")