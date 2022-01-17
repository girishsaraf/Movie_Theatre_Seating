from exceptions import AllocationException, SeatUpdateException


class MovieSeatAllocator:
    """
    Allocates seats as per requests
    """
    def __init__(self):
        """
        Initialize the theatre layout
        Initialize the number of rows and number of seats per row
        """
        self.num_rows = 10
        self.num_seats = 20
        self.theatre_layout = {
            chr(row_name): [0 for _ in range(1, self.num_seats + 1)] for row_name in range(65 + self.num_rows - 1, 65 - 1, -1)
        }
        self.num_allocations = {chr(row_name): 0 for row_name in range(65 + self.num_rows - 1, 65 - 1, -1)}

    def allocate_seats(self, request_id, num_seats_requested):
        """
        :param request_id: ID of the request
        :param num_seats_requested: Seats requested in each request
        :return: Final request with allocated seats
        """
        try:
            if num_seats_requested > self.num_seats:
                error = "Too many seats requested"
                return " ".join([request_id, error])
            if num_seats_requested == 0:
                error = "No Seats requested"
                return " ".join([request_id, error])
            else:
                row = self.get_best_seats(num_seats_requested)
                if row:
                    start_index = self.update_row(row, num_seats_requested)
                    seats_alloted = ','.join([row + str(index) for index in range(start_index, start_index+num_seats_requested)])
                    return " ".join([request_id, seats_alloted])
                else:
                    error = "No space to accomodate request"
                    return " ".join([request_id, error])
        except Exception as e:
            raise AllocationException('Error in allocating seats: {}'.format(str(e)))

    def get_best_seats(self, num_seats_requested):
        """
        :param num_seats_requested: Total seats requested
        :return: Row name where seat was allocated
        """
        for row_name, seats in self.theatre_layout.items():
            num_allocations = self.num_allocations[row_name]
            if seats.count(0) >= num_seats_requested + (3*num_allocations):
                return row_name
        return None

    def update_row(self, row_name, num_seats):
        """
        :param row_name: Row name to be updated
        :param num_seats: Number of seats to be filled
        :return: Last seat filled in the row
        """
        try:
            seats = self.theatre_layout[row_name]
            num_allocations = self.num_allocations[row_name]
            if num_allocations == 0:
                for i in range(len(seats) - 1, len(seats) - num_seats - 1, -1):
                    seats[i] = 1
                self.num_allocations[row_name] += 1
                return len(seats) - num_seats + 1
            else:
                count_spaces = 0
                for i in range(len(seats) - 1, -1, -1):
                    if seats[i:i-3:-1] == [0,0,0]:
                        count_spaces += 1
                        if count_spaces == num_allocations:
                            for seat_index in range(i-3, i-3-num_seats, -1):
                                seats[seat_index] = 1
                            self.num_allocations[row_name] += 1
                            return i-2-num_seats
        except Exception as e:
            raise SeatUpdateException("Error while updating Theatre Layout: {}".format(str(e)))