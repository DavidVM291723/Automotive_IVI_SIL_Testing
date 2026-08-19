Feature: Vehicle Location Telemetry and GPS Tracking
  As a Telematics Systems Engineer
  I want to stream NMEA satellite coordinate sequences over the CAN network
  To verify that the Android LocationManager processes live navigation positioning

  Scenario: Broadcast city route tracking coordinates to the central navigation map
    Given the Android Automotive emulator is active and responsive
    When the telematics control unit streams an active cross-city coordinate route
    Then the Android LocationManager must parse and update the active geographic positioning
