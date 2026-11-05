# Flight Booking Management System

A beginner-friendly, robust, and interactive console application built with **Python 3**, **Object-Oriented Programming (OOP)**, **Pandas**, and **CSV**. 

This system allows passengers to search available flights, book tickets with automatic fare calculation, cancel existing bookings, and view all active and cancelled reservations, with all changes persistent across application restarts.

---

## 📋 Table of Contents
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Class Architecture & OOP Design](#-class-architecture--oop-design)
- [Installation & Setup](#-installation--setup)
- [How to Run in VS Code Terminal](#-how-to-run-in-vs-code-terminal)
- [How to Use the System](#-how-to-use-the-system)
- [Assignment Test Cases](#-assignment-test-cases)
- [Automated Testing](#-automated-testing)
- [Data Persistence & Consistency](#-data-persistence--consistency)

---

## ✈️ Features

1. **Search Flights**:
   - Case-insensitive search by origin and destination cities (e.g., searching for `raipur` and `delhi` finds `Raipur` to `Delhi`).
   - Displays Flight Number, Origin, Destination, Available Seats, and Fare per seat in a clean table.
   - Shows clear feedback when no flights match the criteria.

2. **Book Tickets**:
   - Select flight number, passenger name, and number of seats.
   - Automatically computes total fare using the formula:
     $$\text{Total Fare} = \text{Number of Seats} \times \text{Fare per Seat}$$
   - Generates unique, sequential Booking IDs (`BK1`, `BK2`, `BK3`, etc.).
   - Decrements available seats immediately and confirms reservation details.
   - **Input Validation**:
     - Prevents booking $\le 0$ seats (`"Number of seats must be at least 1."`).
     - Prevents booking on a fully booked flight (`"Flight is full."`).
     - Prevents booking more seats than available (`"Only X seats are available."`).
     - Rejects non-existent flight numbers and blank passenger names.

3. **Cancel Booking**:
   - Cancels reservations by Booking ID.
   - Restores cancelled seats directly to the corresponding flight.
   - Updates booking status to `Cancelled`.
   - Prevents duplicate cancellations on already cancelled bookings.

4. **View All Bookings**:
   - Formatted tabular display of all bookings with Booking ID, Flight Number, Passenger Name, Seats, Total Fare, and Status (`Confirmed` or `Cancelled`).

5. **Fault-Tolerant CSV Data Loading with Pandas**:
   - Gracefully handles missing files, empty files, missing values (`NaN`), and corrupt rows without crashing.
   - Reports the total number of valid flight records loaded on startup.

---

## 🛠️ Technologies Used

- **Python 3.12+**
- **Pandas**: Efficient CSV file reading, data validation, and manipulation.
- **CSV**: Persistent storage for flight schedules and passenger bookings.
- **Object-Oriented Programming (OOP)**: Encapsulation with dedicated classes (`Flight`, `FlightBookingSystem`).
- **Standard Library Modules**: `os`, `sys`.

---

## 📁 Project Structure

```text
Flight_Booking_System/
├── main.py              # Main interactive menu-driven application
├── flights.csv          # Flight records (FlightNo, Origin, Destination, Seats, Fare)
├── bookings.csv         # Booking history (BookingID, FlightNo, PassengerName, Seats, TotalFare, Status)
├── requirements.txt     # Python package dependencies (pandas)
├── test_cases.py        # Automated test suite covering Test Cases 1 - 4 & persistence
└── README.md            # Comprehensive project documentation
```

---

## 🏛️ Class Architecture & OOP Design

### 1. `Flight` Class
Represents a single flight and its seat inventory.
- **Attributes**:
  - `flight_no` (str): Identifier (e.g., `"A1101"`).
  - `origin` (str): Departure city (e.g., `"Raipur"`).
  - `destination` (str): Arrival city (e.g., `"Delhi"`).
  - `seats` (int): Current available seat count.
  - `fare` (float): Ticket price per seat.
- **Methods**:
  - `display_details()`: Displays formatted flight summary.
  - `check_availability(required_seats)`: Validates availability against business rules.
  - `book_seats(num_seats)`: Deducts booked seats from available inventory.
  - `cancel_seats(num_seats)`: Restores cancelled seats to available inventory.

### 2. `FlightBookingSystem` Class
Manages the application's business logic, user operations, and persistent storage.
- **Attributes**:
  - `flights_file`: Path to `flights.csv`.
  - `bookings_file`: Path to `bookings.csv`.
  - `flights`: List of `Flight` instances.
  - `bookings`: List of booking dictionaries.
  - `next_booking_counter`: Integer tracking the next unique booking ID.
- **Methods**:
  - `load_flights()`: Loads and cleans flight data using Pandas.
  - `save_flights()`: Persists seat inventory updates back to `flights.csv`.
  - `load_bookings()`: Loads existing booking records from `bookings.csv`.
  - `save_bookings()`: Persists bookings and cancellations to `bookings.csv`.
  - `search_flights(origin, destination)`: Case-insensitive city search.
  - `book_ticket(flight_no, passenger_name, num_seats)`: Processes ticket reservations.
  - `cancel_booking(booking_id)`: Handles ticket cancellations and restores inventory.
  - `view_all_bookings()`: Displays all bookings.

---

## ⚙️ Installation & Setup

### Prerequisites
Make sure Python 3 is installed on your computer. You can check in your terminal:
```bash
python --version
```

### Step 1: Open the Project Directory
Navigate to the project folder:
```bash
cd "C:\Users\Chetna\.gemini\antigravity\scratch\Flight_Booking_System"
```

### Step 2: Install Dependencies
Install required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run in VS Code Terminal

1. **Open VS Code**.
2. Go to **File** > **Open Folder...** and select:
   ```
   C:\Users\Chetna\.gemini\antigravity\scratch\Flight_Booking_System
   ```
3. Open the built-in terminal in VS Code:
   - Press <kbd>Ctrl</kbd> + <kbd>`</kbd> (Backtick), or
   - Select **Terminal** > **New Terminal** from the top menu.
4. Run the application:
   ```bash
   python main.py
   ```
5. Follow the interactive numbered menu prompts!

---

## 📖 How to Use the System

When launched, the program displays the main menu:

```text
===== FLIGHT BOOKING MANAGEMENT SYSTEM =====
1. Search Flights
2. Book Tickets
3. Cancel Booking
4. View All Bookings
5. Exit

Enter your choice: 
```

### Option 1: Search Flights
- Enter the origin and destination city.
- The search is case-insensitive (e.g., `raipur` or `RAIPUR`).
- Displays matching flights with available seats and fares.

### Option 2: Book Tickets
- Enter flight number (e.g., `A1101`), passenger name, and number of seats.
- If seats are available, your booking will be confirmed with a unique ID (e.g., `BK1`) and the total fare will be calculated.
- If the flight is full, seats are insufficient, or the input is $\le 0$, an informative error message will be shown.

### Option 3: Cancel Booking
- Enter the Booking ID (e.g., `BK1`).
- The booking status is changed to `Cancelled`, and the seats are returned to the flight.
- Attempting to cancel an already cancelled ticket is prevented.

### Option 4: View All Bookings
- Shows a list of all reservations made along with their current status (`Confirmed` or `Cancelled`).

### Option 5: Exit
- Exits the application cleanly. All changes are already safely saved to the CSV files.

---

## 🧪 Assignment Test Cases

The application is thoroughly verified against all four specified test cases:

### Test Case 1: Normal Input (Search)
- **Input**: Origin: `Raipur`, Destination: `Delhi`
- **Expected Output**: Flight `A1101` found, 5 seats available, fare Rs. 6000.
- **Status**: ✅ Passed

### Test Case 2: Boundary Input (Full Capacity Booking)
- **Input**: Book Flight: `A1202`, Passenger: `Kiran Rao`, Seats: `2`
- **Expected Output**:
  - Booking ID: `BK1`
  - Total Fare: Rs. 11000
  - Remaining seats: 0
- **Status**: ✅ Passed

### Test Case 3: Invalid Input Validation
- **(a) Book 1 seat on A1303**:
  - Available seats: 0
  - Expected Output: `Flight is full.`
  - **Status**: ✅ Passed
- **(b) Book 6 seats on A1101**:
  - Available seats: 5
  - Expected Output: `Only 5 seats are available.`
  - **Status**: ✅ Passed
- **(c) Book 0 seats on A1101**:
  - Requested seats: 0
  - Expected Output: `Number of seats must be at least 1.`
  - **Status**: ✅ Passed

### Test Case 4: Booking & Cancellation
- **(a) Book Flight `A1101`**:
  - Passenger: `Priya Nair`, Seats: `3`
  - Expected Output: Booking ID: `BK1`, Total: Rs. 18000, Remaining seats: 2
- **(b) Cancel Booking `BK1`**:
  - Expected Output: Booking cancelled, Seats left on `A1101`: 5
- **Status**: ✅ Passed

---

## 🤖 Automated Testing

An automated test script `test_cases.py` is included to run all 4 test cases and test persistence independently.

To run the automated tests:
```bash
python test_cases.py
```

Sample output:
```text
============================================================
ALL TEST CASES PASSED SUCCESSFULLY!
Original data files have been restored for application use.
============================================================
```

---

## 🔄 Data Persistence & Consistency

- **Real-time Sync**: Whenever a ticket is booked or cancelled, both `flights.csv` and `bookings.csv` are updated immediately.
- **No Double-Counting**: When restarted, `flights.csv` already contains the correct current seat counts. The system does not re-apply active bookings or cancellations onto `flights.csv`, preventing any seat count inflation or double-counting errors.
- **Sequential IDs**: When restarted, the system scans existing records in `bookings.csv` and starts issuing IDs following the highest existing ID number (e.g., if `BK1` and `BK2` exist, the next is `BK3`).
