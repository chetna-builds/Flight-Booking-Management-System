"""
Test Suite for Flight Booking Management System
================================================
Verifies all 4 required test cases independently using the original flight data:
1. Normal Input (Search)
2. Boundary Input (Booking all remaining seats)
3. Invalid Input (Full flight, over-capacity, 0 seats)
4. Valid Scenario (Booking and Cancellation)
"""

import os
import sys
import io

# Import the system classes from main
from main import Flight, FlightBookingSystem

ORIGINAL_FLIGHTS_CSV = """FlightNo,Origin,Destination,Seats,Fare
A1101,Raipur,Delhi,5,6000
A1202,Raipur,Mumbai,2,5500
A1303,Delhi,Mumbai,0,4800
"""

def reset_data_files():
    """Resets flights.csv and bookings.csv to their initial states."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    flights_file = os.path.join(base_dir, "flights.csv")
    bookings_file = os.path.join(base_dir, "bookings.csv")

    with open(flights_file, "w", encoding="utf-8") as f:
        f.write(ORIGINAL_FLIGHTS_CSV.strip() + "\n")

    with open(bookings_file, "w", encoding="utf-8") as f:
        f.write("BookingID,FlightNo,PassengerName,Seats,TotalFare,Status\n")

    return flights_file, bookings_file


def run_test_case_1():
    print("\n" + "=" * 60)
    print("RUNNING TEST CASE 1: Normal Input (Search)")
    print("=" * 60)
    reset_data_files()
    system = FlightBookingSystem()

    # Search: Origin: Raipur, Destination: Delhi
    results = system.search_flights("Raipur", "Delhi")

    assert len(results) == 1, f"Expected 1 flight, found {len(results)}"
    flight = results[0]
    assert flight.flight_no == "A1101", f"Expected A1101, got {flight.flight_no}"
    assert flight.seats == 5, f"Expected 5 seats, got {flight.seats}"
    assert flight.fare == 6000, f"Expected fare 6000, got {flight.fare}"

    print(">> TEST CASE 1 PASSED: A1101 found, 5 seats available, fare Rs. 6000.")


def run_test_case_2():
    print("\n" + "=" * 60)
    print("RUNNING TEST CASE 2: Boundary Input (Book all seats)")
    print("=" * 60)
    reset_data_files()
    system = FlightBookingSystem()

    # Book: Flight: A1202, Passenger: Kiran Rao, Seats: 2
    booking = system.book_ticket("A1202", "Kiran Rao", 2)

    assert booking is not None, "Booking failed unexpectedly"
    assert booking["BookingID"] == "BK1", f"Expected Booking ID BK1, got {booking['BookingID']}"
    assert booking["TotalFare"] == 11000, f"Expected Total Rs. 11000, got {booking['TotalFare']}"
    
    flight = system.find_flight("A1202")
    assert flight.seats == 0, f"Expected 0 remaining seats, got {flight.seats}"

    print(">> TEST CASE 2 PASSED: Booking ID BK1, Total: Rs. 11000, Remaining seats: 0.")


def run_test_case_3():
    print("\n" + "=" * 60)
    print("RUNNING TEST CASE 3: Invalid Input")
    print("=" * 60)
    reset_data_files()
    system = FlightBookingSystem()

    # (a) Book 1 seat on A1303 (Flight is full)
    flight_a1303 = system.find_flight("A1303")
    is_avail_a, msg_a = flight_a1303.check_availability(1)
    print(f"(a) Booking 1 seat on A1303 -> Result: {msg_a}")
    assert not is_avail_a and msg_a == "Flight is full.", f"Unexpected result: {msg_a}"

    # (b) Book 6 seats on A1101 (Only 5 seats available)
    flight_a1101 = system.find_flight("A1101")
    is_avail_b, msg_b = flight_a1101.check_availability(6)
    print(f"(b) Booking 6 seats on A1101 -> Result: {msg_b}")
    assert not is_avail_b and msg_b == "Only 5 seats are available.", f"Unexpected result: {msg_b}"

    # (c) Book 0 seats on A1101 (Seats must be at least 1)
    is_avail_c, msg_c = flight_a1101.check_availability(0)
    print(f"(c) Booking 0 seats on A1101 -> Result: {msg_c}")
    assert not is_avail_c and msg_c == "Number of seats must be at least 1.", f"Unexpected result: {msg_c}"

    print(">> TEST CASE 3 PASSED: All invalid input checks verified correctly.")


def run_test_case_4():
    print("\n" + "=" * 60)
    print("RUNNING TEST CASE 4: Different Valid Scenario & Cancellation")
    print("=" * 60)
    reset_data_files()
    system = FlightBookingSystem()

    # (a) Book: Flight: A1101, Passenger: Priya Nair, Seats: 3
    booking = system.book_ticket("A1101", "Priya Nair", 3)
    assert booking is not None, "Booking failed unexpectedly"
    assert booking["BookingID"] == "BK1", f"Expected Booking ID BK1, got {booking['BookingID']}"
    assert booking["TotalFare"] == 18000, f"Expected Total Rs. 18000, got {booking['TotalFare']}"

    flight = system.find_flight("A1101")
    assert flight.seats == 2, f"Expected remaining seats 2, got {flight.seats}"
    print(f"(a) Booking BK1 created, Total Rs. 18000, Remaining seats on A1101: {flight.seats}")

    # (b) Cancel booking BK1
    cancelled = system.cancel_booking("BK1")
    assert cancelled is True, "Cancellation failed"
    assert flight.seats == 5, f"Expected seats left on A1101 to be 5, got {flight.seats}"
    print(f"(b) Booking BK1 cancelled successfully. Seats left on A1101: {flight.seats}")

    # Also verify that BK1 cannot be cancelled twice
    cancelled_again = system.cancel_booking("BK1")
    assert cancelled_again is False, "Should not be able to cancel twice"
    print("Verified: Booking BK1 cannot be cancelled twice.")

    print(">> TEST CASE 4 PASSED: Booking and Cancellation fully verified.")


def run_persistence_test():
    print("\n" + "=" * 60)
    print("RUNNING DATA PERSISTENCE & CONSISTENCY TEST")
    print("=" * 60)
    reset_data_files()

    # Session 1: Book tickets
    system1 = FlightBookingSystem()
    system1.book_ticket("A1101", "Alice", 2)  # Seats left: 3, BK1
    system1.book_ticket("A1202", "Bob", 1)    # Seats left: 1, BK2

    # Session 2: Reload application
    system2 = FlightBookingSystem()
    f1 = system2.find_flight("A1101")
    f2 = system2.find_flight("A1202")
    assert f1.seats == 3, f"Persisted seats for A1101 expected 3, got {f1.seats}"
    assert f2.seats == 1, f"Persisted seats for A1202 expected 1, got {f2.seats}"
    assert len(system2.bookings) == 2, f"Expected 2 bookings, got {len(system2.bookings)}"
    assert system2.next_booking_counter == 3, f"Expected next booking counter 3, got {system2.next_booking_counter}"

    # Cancel in Session 2
    system2.cancel_booking("BK1")
    assert f1.seats == 5, f"After cancel, A1101 seats expected 5, got {f1.seats}"

    # Session 3: Reload again to verify cancelled state persisted
    system3 = FlightBookingSystem()
    f1_reloaded = system3.find_flight("A1101")
    assert f1_reloaded.seats == 5, f"After reload, A1101 seats expected 5, got {f1_reloaded.seats}"
    bk1 = next(b for b in system3.bookings if b["BookingID"] == "BK1")
    assert bk1["Status"] == "Cancelled", "Booking status should be Cancelled"

    print(">> PERSISTENCE TEST PASSED: State preserved across restarts without double-counting.")


if __name__ == "__main__":
    run_test_case_1()
    run_test_case_2()
    run_test_case_3()
    run_test_case_4()
    run_persistence_test()

    # Reset data files back to original clean state after tests
    reset_data_files()
    print("\n" + "=" * 60)
    print("ALL TEST CASES PASSED SUCCESSFULLY!")
    print("Original data files have been restored for application use.")
    print("=" * 60)
