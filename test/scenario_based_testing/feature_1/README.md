<div align="center">
  <h1 style="font-size: 36px;">Feature: Users can book and cancel a shuttle via the smartwatch and interact with the internal user interface for health monitoring and calling a doctor. </h1>
</div>


## Feature Owner: Mahitha Balachandran Sheeja

## 📚 Contents
- [Feature Overview](#feature-overview)
- [Test Strategy](#test-strategy)
- [Evaluation](#evaluation)

## Feature Overview
This feature enables users to book and cancel an autonomous shuttle through a smartwatch application and interact with the internal user interface for health-related support. The smartwatch provides a simple and controlled interaction flow for creating and managing shuttle trips. Once inside the shuttle, the internal user interface allows users to monitor basic health information and request assistance, such as calling a doctor if needed. The feature ensures seamless communication between the smartwatch, backend system, and autonomous shuttle platform while maintaining consistent system states and safe operation.

**Key Performance Indicators (KPIs)**
1. Booking success reliability: Booking requests initiated via the smartwatch are successfully processed and confirmed by the system.
2. Cancellation response time: The time between user confirmation of cancellation and system acknowledgment remains within acceptable limits.
3. State consistency: Booking and cancellation actions result in consistent system states across the smartwatch, backend server, and autonomous shuttle.
4. User feedback clarity: The smartwatch user interface provides clear and timely feedback for booking confirmation and trip cancellation.
5. Single processing guarantee: Each booking or cancellation request is processed exactly once, preventing duplicate or unintended actions

**Feature Functionality / Properties**

The Smartwatch-Based Shuttle Booking and Cancellation feature enables users to create and manage shuttle bookings through a smartwatch application in a controlled and reliable manner.

1. Users can book a shuttle via the smartwatch when no active booking exists.
2. After successful booking confirmation, the system enters an active booking state.
3. A cancellation option is available only after booking confirmation and requires explicit user confirmation.
4. Cancellation requests are propagated to the backend server and the autonomous shuttle system via ROS 2 communication.
5. The autonomous decision core acknowledges the cancellation and safely terminates the ongoing trip, if active.
6. After successful cancellation, all booking-related states are reset, and the smartwatch user interface returns to the home screen.
7. The system ensures that each booking and cancellation request is processed exactly once.


## Test Strategy
Detailed Test Strategy document can be found [here](https://drive.google.com/file/d/1MXbT3ACCZax9bBI6pCZO7Rd5jiHhAYvC/view?usp=drive_link).

## Evaluation
Detailed evaluation is documented in [Test Specification](https://git.hs-coburg.de/pax_auto/pax_auto_main/src/branch/main/test/scenario_based_testing/feature_1/BC_Test_Specification_%20EN.xlsx) document.





