# Flight App
### Problem Specifications
Design and implement an application to reserve flights based on source, destination
and date. The application should take care of the following aspects:
  - Repository of flight information containing airline name, flight number, source,
  destination, start time, end time, frequency (days on which the flight is
  active), total number of seats in the aircraft (capacity)
  - Ability to search for flights based on source, destination and date
  - Reserve 'n' number of seats on a particular fight based on availability of
seats. <br/>
**APIs**:
  1. Search for flights based on source, destination and date
  2. User being able to reserve 'n' number of seats on a particular fight (this API
  should keep availability of seats on that flight in mind)
  3. View reservations for a users (both past and upcoming)
### Dependencies
1. Flask
2. Python 3.0
