
## Assumptions

- The train has only the one type of reserved seat.
- The number of stops for each train would be max 50.
- The number of seats in each train would be max 2000.
- The booking can only be made only if seat is available.
- The number of fetching seats info is more than booking made.
- When a user search trains between two station we are assuming that there 
  would be maximum 30 trains would be there.

seat rows for each train = 30 * 50 * 2000 = 30,00,000

## Idea 3

Two ways:

1. Station only will record whether a seat is booked for a station.

    ```
    Train:
      name: String
      seats_count: Integer = 0

    Stops:
      name: String
      train: Train
      seats_booked: Integer[] = []
      arrival_time: Datetime
      departure_time: Datetime 
    ```

2. First define a seat table which will record seat booked for each stops.

    ```
    Train:
      name: String

    Seats:
      number: Integer
      train: Train
      booked_for: Stop[] = []

    Stops:
      name: String
      train: Train
      arrival_time: Datetime
      departure_time: Datetime 
    ```
