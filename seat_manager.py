import csv
import os

from config import SEAT_FOLDER


# =========================================
# CREATE SEAT FOLDER
# =========================================

def create_seat_folder():
    if not os.path.exists(SEAT_FOLDER):
        os.makedirs(SEAT_FOLDER)


# =========================================
# GET CSV FILE PATH
# =========================================

def get_file_path(filename):
    create_seat_folder()
    return os.path.join(
        SEAT_FOLDER,
        filename
    )


# =========================================
# CREATE SEAT MATRIX
# =========================================

def create_seat_matrix(
    filename,
    number_of_rows,
    columns
):

    filepath = get_file_path(filename)
    with open(filepath,"w",newline="") as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(["Seat"] + columns)
        # Rows
        for row in range(1,number_of_rows + 1):
            writer.writerow([row]+["Available"] * len(columns))
    return filepath


# =========================================
# READ SEAT MATRIX
# =========================================

def read_seat_matrix(filename):
    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return None, None

    with open(filepath,"r",newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) == 0:
        return None, None
    header = rows[0]
    data = rows[1:]
    return header, data


# =========================================
# DISPLAY SEAT MATRIX
# =========================================

def display_seat_matrix(filename):
    header, data = read_seat_matrix(filename)
    if header is None:
        print("Seat matrix not found.")
        return

    print("\n")
    print("=" * 75)
    print("                     SEAT MATRIX")
    print("=" * 75)

    print(
        "       "+" | ".join(f"{column:^12}"for column in header[1:])
    )

    print("-" * 75)
    for row in data:
        print(
            f"{row[0]:>3}    "+" | ".join(f"{status:^12}"for status in row[1:])
        )

    print("=" * 75)


# =========================================
# GET SEAT STATUS
# =========================================

def get_seat_status(
    filename,
    seat_number
):

    header, data = read_seat_matrix(filename)
    if header is None:
        return None
    seat_number = seat_number.upper()
    try:
        row_number = int(
            seat_number[:-1]
        )
        column = seat_number[-1]
        column_index = header.index(
            column
        )

    except (ValueError, IndexError):
        return None

    for row in data:
        if int(row[0]) == row_number:
            return row[column_index]

    return None


# =========================================
# UPDATE SEAT STATUS
# =========================================

def update_seat_status(
    filename,
    seat_number,
    new_status
):
    header, data = read_seat_matrix(filename)
    if header is None:
        return False
    seat_number = seat_number.upper()
    try:
        row_number = int(
            seat_number[:-1]
        )
        column = seat_number[-1]
        column_index = header.index(
            column
        )

    except (ValueError, IndexError):
        return False
    
    for row in data:
        if int(row[0]) == row_number:
            current_status = row[
                column_index
            ]
            if (
                current_status == "Available"
                and
                new_status == "Booked"
            ):
                row[column_index] = "Booked"

            elif (
                current_status == "Booked"
                and
                new_status == "Available"
            ):
                row[column_index] = "Available"

            else:
                return False

            break

    filepath = get_file_path(filename)
    with open(
        filepath,"w",newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    return True


# =========================================
# COUNT AVAILABLE SEATS
# =========================================

def count_available_seats(filename):
    header, data = read_seat_matrix(filename)
    if header is None:
        return 0
    count = 0
    for row in data:
        for value in row[1:]:
            if value == "Available":
                count += 1

    return count