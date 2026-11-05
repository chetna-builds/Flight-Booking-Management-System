"""
Flight Booking Management System
================================
A beginner-friendly, menu-driven Python application for managing flight
searches, ticket bookings, and ticket cancellations using OOP, Pandas, and CSV.
"""

import os
import pandas as pd


class Flight:
    """
    Represents an individual flight with its attributes and seat operations.
    """

    def __init__(self, flight_no, origin, destination, seats, fare):
        """
        Initializes a Flight instance.
        
        Parameters:
            flight_no (str): Unique flight identifier (e.g., A1101)
            origin (str): Departure city
            destination (str): Arrival city
            seats (int): Number of currently available seats
            fare (float/int): Price per seat in Rupees
        """
        self.flight_no = str(flight_no).strip().upper()
        self.origin = str(origin).strip()
        self.destination = str(destination).strip()
        self.seats = int(seats)
        self.fare = float(fare)

    def display_details(self):
        """Displays formatted details of this flight."""
        print(f"Flight No       : {self.flight_no}")
        print(f"Origin          : {self.origin}")
        print(f"Destination     : {self.destination}")
        print(f"Available Seats : {self.seats}")
        print(f"Fare per Seat   : Rs. {self.fare:.0f}")

    def check_availability(self, required_seats):
        """
        Checks whether the requested number of seats can be booked.
        
        Returns:
            tuple: (is_available (bool), reason_or_message (str))
        """
        # Rule 1: Cannot book 0 or negative seats
        if required_seats <= 0:
            return False, "Number of seats must be at least 1."

        # Rule 2: Cannot book on a flight that has 0 available seats
        if self.seats == 0:
            return False, "Flight is full."

        # Rule 3: Cannot book more seats than available
        if required_seats > self.seats:
            return False, f"Only {self.seats} seats are available."

        # Rule 4: Seats are available
        return True, "Seats available."

    def book_seats(self, num_seats):
        """
        Deducts booked seats from currently available seats.
        """
        self.seats -= num_seats

    def cancel_seats(self, num_seats):
        """
        Restores cancelled seats back to available seats.
        """
        self.seats += num_seats


class FlightBookingSystem:
    """
    Manages the overall flight operations: searching, booking, cancelling,
    viewing bookings, and persisting data to CSV files using Pandas.
    """

    DEFAULT_FLIGHTS_DATA = """FlightNo,Origin,Destination,Seats,Fare
A1101,Raipur,Delhi,5,6000
A1202,Raipur,Mumbai,2,5500
A1303,Delhi,Mumbai,0,4800
"""

    def __init__(self, flights_file="flights.csv", bookings_file="bookings.csv"):
        """
        Initializes the booking system, sets file paths, and loads data.
        """
        # Resolve absolute paths based on this script's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.flights_file = os.path.join(base_dir, flights_file)
        self.bookings_file = os.path.join(base_dir, bookings_file)

        self.flights = []          # List of Flight objects
        self.bookings = []         # List of booking dictionaries
        self.next_booking_counter = 1  # Counter for generating unique IDs (BK1, BK2, ...)

        # Load existing data on startup
        self.load_flights()
        self.load_bookings()

    def create_default_flights_file(self):
        """Creates the default flights.csv file if it does not exist."""
        try:
            with open(self.flights_file, "w", encoding="utf-8") as f:
                f.write(self.DEFAULT_FLIGHTS_DATA.strip() + "\n")
            print(f"[Info] Default '{os.path.basename(self.flights_file)}' created successfully.")
        except Exception as e:
            print(f"[Error] Failed to create default flights file: {e}")

    def load_flights(self):
        """
        Reads flight data from flights.csv using Pandas.
        Handles missing files, empty files, missing values, and invalid rows safely.
        """
        self.flights = []

        # 1. Handle missing file
        if not os.path.exists(self.flights_file):
            print(f"[Warning] '{os.path.basename(self.flights_file)}' not found.")
            self.create_default_flights_file()

        # 2. Handle empty file
        if os.path.getsize(self.flights_file) == 0:
            print(f"[Warning] '{os.path.basename(self.flights_file)}' is empty. Recreating default data...")
            self.create_default_flights_file()

        try:
            # Read CSV using Pandas
            df = pd.read_csv(self.flights_file)

            # Check for required columns
            required_cols = {"FlightNo", "Origin", "Destination", "Seats", "Fare"}
            if not required_cols.issubset(df.columns):
                print(f"[Error] Missing required columns in CSV! Expected: {required_cols}")
                return

            # Clean rows: remove rows where any required field is missing (NaN)
            df_clean = df.dropna(subset=list(required_cols))

            valid_flights = []
            for index, row in df_clean.iterrows():
                try:
                    flight_no = str(row["FlightNo"]).strip().upper()
                    origin = str(row["Origin"]).strip()
                    dest = str(row["Destination"]).strip()
                    seats = int(row["Seats"])
                    fare = float(row["Fare"])

                    # Logic check: seats and fare cannot be negative, strings cannot be empty
                    if not flight_no or not origin or not dest or seats < 0 or fare < 0:
                        print(f"[Notice] Skipping invalid flight record at row {index + 2}.")
                        continue

                    flight_obj = Flight(flight_no, origin, dest, seats, fare)
                    valid_flights.append(flight_obj)

                except (ValueError, TypeError):
                    print(f"[Notice] Skipping malformed flight data at row {index + 2}.")
                    continue

            self.flights = valid_flights
            print(f"Total valid flight records loaded: {len(self.flights)}")

        except pd.errors.EmptyDataError:
            print(f"[Error] '{os.path.basename(self.flights_file)}' contains no data.")
        except Exception as e:
            print(f"[Error] An unexpected error occurred while loading flights: {e}")

    def save_flights(self):
        """
        Saves current flight data back to flights.csv using Pandas.
        Keeps seat counts consistent across application runs.
        """
        try:
            records = []
            for flight in self.flights:
                records.append({
                    "FlightNo": flight.flight_no,
                    "Origin": flight.origin,
                    "Destination": flight.destination,
                    "Seats": flight.seats,
                    "Fare": int(flight.fare) if flight.fare.is_integer() else flight.fare
                })
            df = pd.DataFrame(records)
            df.to_csv(self.flights_file, index=False)
        except Exception as e:
            print(f"[Error] Failed to save flight data: {e}")

    def load_bookings(self):
        """
        Reads existing booking records from bookings.csv.
        Restores previous bookings and determines the next unique Booking ID.
        """
        self.bookings = []
        if not os.path.exists(self.bookings_file) or os.path.getsize(self.bookings_file) == 0:
            return

        try:
            df = pd.read_csv(self.bookings_file)
            required_cols = {"BookingID", "FlightNo", "PassengerName", "Seats", "TotalFare", "Status"}
            if not required_cols.issubset(df.columns):
                return

            max_counter = 0
            for _, row in df.iterrows():
                b_id = str(row["BookingID"]).strip()
                booking = {
                    "BookingID": b_id,
                    "FlightNo": str(row["FlightNo"]).strip().upper(),
                    "PassengerName": str(row["PassengerName"]).strip(),
                    "Seats": int(row["Seats"]),
                    "TotalFare": float(row["TotalFare"]),
                    "Status": str(row["Status"]).strip()
                }
                self.bookings.append(booking)

                # Extract numeric counter from IDs formatted like 'BK1', 'BK2', etc.
                if b_id.upper().startswith("BK"):
                    num_part = b_id[2:]
                    if num_part.isdigit():
                        max_counter = max(max_counter, int(num_part))

            self.next_booking_counter = max_counter + 1

        except Exception as e:
            print(f"[Notice] Could not load previous bookings: {e}")

    def save_bookings(self):
        """
        Saves booking records back to bookings.csv using Pandas.
        Preserves bookings and cancellations when the app restarts.
        """
        try:
            if not self.bookings:
                # Create empty bookings file with header
                empty_df = pd.DataFrame(columns=["BookingID", "FlightNo", "PassengerName", "Seats", "TotalFare", "Status"])
                empty_df.to_csv(self.bookings_file, index=False)
                return

            df = pd.DataFrame(self.bookings)
            df.to_csv(self.bookings_file, index=False)
        except Exception as e:
            print(f"[Error] Failed to save bookings: {e}")

    def find_flight(self, flight_no):
        """
        Finds a flight object by flight number (case-insensitive).
        Returns Flight object or None.
        """
        flight_no_clean = str(flight_no).strip().upper()
        for flight in self.flights:
            if flight.flight_no == flight_no_clean:
                return flight
        return None

    def search_flights(self, origin, destination):
        """
        Searches flights matching origin and destination (case-insensitive).
        Displays matching flight details in a clear tabular format.
        """
        origin_clean = origin.strip().lower()
        dest_clean = destination.strip().lower()

        matches = []
        for flight in self.flights:
            if flight.origin.lower() == origin_clean and flight.destination.lower() == dest_clean:
                matches.append(flight)

        print("\n" + "=" * 68)
        print("                        SEARCH RESULTS")
        print("=" * 68)

        if not matches:
            print(f"No flights found from '{origin.strip()}' to '{destination.strip()}'.")
            print("=" * 68)
            return matches

        # Header
        print(f"{'Flight No':<12}{'Origin':<15}{'Destination':<15}{'Seats':<10}{'Fare/Seat':<12}")
        print("-" * 68)
        for f in matches:
            print(f"{f.flight_no:<12}{f.origin:<15}{f.destination:<15}{f.seats:<10}Rs. {f.fare:<10.0f}")
        print("=" * 68)
        return matches

    def book_ticket(self, flight_no, passenger_name, num_seats):
        """
        Handles ticket booking process:
        - Validates flight existence
        - Validates requested seats
        - Calculates total fare automatically
        - Generates unique booking ID (BK1, BK2, ...)
        - Deducts seats and saves changes to CSV files
        
        Returns:
            dict or None: The confirmed booking record, or None on failure.
        """
        flight = self.find_flight(flight_no)
        if not flight:
            print(f"\n[Error] Invalid flight number! Flight '{flight_no.strip().upper()}' not found.")
            return None

        # Check passenger name
        clean_name = passenger_name.strip()
        if not clean_name:
            print("\n[Error] Passenger name cannot be empty.")
            return None

        # Check seat availability using Flight method
        is_available, message = flight.check_availability(num_seats)
        if not is_available:
            print(f"\n[Error] {message}")
            return None

        # Calculate Total Fare = Seats * Fare per Seat
        total_fare = num_seats * flight.fare

        # Generate unique booking ID
        booking_id = f"BK{self.next_booking_counter}"
        self.next_booking_counter += 1

        # Deduct seats from the flight
        flight.book_seats(num_seats)

        # Create booking record
        booking_record = {
            "BookingID": booking_id,
            "FlightNo": flight.flight_no,
            "PassengerName": clean_name,
            "Seats": num_seats,
            "TotalFare": total_fare,
            "Status": "Confirmed"
        }
        self.bookings.append(booking_record)

        # Save changes to both CSV files
        self.save_flights()
        self.save_bookings()

        # Display booking confirmation
        print("\n" + "=" * 50)
        print("             BOOKING CONFIRMATION")
        print("=" * 50)
        print(f"Booking ID      : {booking_id}")
        print(f"Flight Number   : {flight.flight_no}")
        print(f"Passenger Name  : {clean_name}")
        print(f"Seats Booked    : {num_seats}")
        print(f"Total Fare      : Rs. {total_fare:.0f}")
        print(f"Remaining Seats : {flight.seats}")
        print("Status          : Confirmed")
        print("=" * 50)

        return booking_record

    def cancel_booking(self, booking_id):
        """
        Cancels an active booking:
        - Verifies booking exists
        - Ensures booking is currently active (not already cancelled)
        - Restores seats to the flight
        - Updates status to 'Cancelled'
        - Saves changes to CSV files
        
        Returns:
            bool: True if cancelled successfully, False otherwise.
        """
        b_id_clean = booking_id.strip().upper()

        # Search for booking
        target_booking = None
        for b in self.bookings:
            if b["BookingID"].upper() == b_id_clean:
                target_booking = b
                break

        if not target_booking:
            print(f"\n[Error] Booking ID '{b_id_clean}' not found.")
            return False

        # Check if already cancelled
        if target_booking["Status"] == "Cancelled":
            print(f"\n[Error] Booking {b_id_clean} is already cancelled. Cannot be cancelled twice.")
            return False

        # Find the flight to restore seats
        flight = self.find_flight(target_booking["FlightNo"])
        if flight:
            flight.cancel_seats(target_booking["Seats"])
            remaining_seats = flight.seats
        else:
            remaining_seats = "N/A"

        # Update status
        target_booking["Status"] = "Cancelled"

        # Save changes to both CSV files
        self.save_flights()
        self.save_bookings()

        print("\n" + "=" * 50)
        print("         BOOKING CANCELLATION SUCCESSFUL")
        print("=" * 50)
        print(f"Booking ID         : {target_booking['BookingID']}")
        print(f"Flight Number      : {target_booking['FlightNo']}")
        print(f"Passenger Name     : {target_booking['PassengerName']}")
        print(f"Seats Cancelled    : {target_booking['Seats']}")
        print(f"Status             : Cancelled")
        if flight:
            print(f"Seats left on {flight.flight_no}: {remaining_seats}")
        print("=" * 50)

        return True

    def view_all_bookings(self):
        """
        Displays all bookings (both Confirmed and Cancelled) in a clean table.
        """
        print("\n" + "=" * 74)
        print("                           ALL BOOKINGS")
        print("=" * 74)

        if not self.bookings:
            print("No bookings found in the system.")
            print("=" * 74)
            return

        print(f"{'Booking ID':<12}{'Flight No':<12}{'Passenger':<20}{'Seats':<8}{'Total (Rs.)':<12}{'Status':<10}")
        print("-" * 74)
        for b in self.bookings:
            print(f"{b['BookingID']:<12}{b['FlightNo']:<12}{b['PassengerName']:<20}{b['Seats']:<8}{b['TotalFare']:<12.0f}{b['Status']:<10}")
        print("=" * 74)


# ==============================================================================
# User Interface & Main Function
# ==============================================================================

def display_menu():
    """Prints the main menu options."""
    print("\n===== FLIGHT BOOKING MANAGEMENT SYSTEM =====")
    print("1. Search Flights")
    print("2. Book Tickets")
    print("3. Cancel Booking")
    print("4. View All Bookings")
    print("5. Exit")


def main():
    """
    Main function to run the interactive console application.
    """
    system = FlightBookingSystem()

    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            print("\n--- Search Flights ---")
            origin = input("Enter Origin City: ").strip()
            destination = input("Enter Destination City: ").strip()

            if not origin or not destination:
                print("[Error] Origin and Destination cannot be empty.")
            else:
                system.search_flights(origin, destination)

        elif choice == "2":
            print("\n--- Book Tickets ---")
            flight_no = input("Enter Flight Number: ").strip()
            passenger_name = input("Enter Passenger Name: ").strip()
            seats_input = input("Enter Number of Seats: ").strip()

            # Handle non-integer seat inputs safely
            try:
                num_seats = int(seats_input)
                system.book_ticket(flight_no, passenger_name, num_seats)
            except ValueError:
                print("[Error] Invalid input! Number of seats must be a valid integer.")

        elif choice == "3":
            print("\n--- Cancel Booking ---")
            booking_id = input("Enter Booking ID to cancel (e.g., BK1): ").strip()
            if not booking_id:
                print("[Error] Booking ID cannot be empty.")
            else:
                system.cancel_booking(booking_id)

        elif choice == "4":
            system.view_all_bookings()

        elif choice == "5":
            print("\nThank you for using Flight Booking Management System. Goodbye!\n")
            break

        else:
            print("[Error] Invalid choice! Please select a valid option (1-5).")


if __name__ == "__main__":
    main()
