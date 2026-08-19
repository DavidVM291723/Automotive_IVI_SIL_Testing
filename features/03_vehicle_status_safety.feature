Feature: Vehicle Status and Safety Interlocks
  As a Powertrain Safety Engineer
  I want to simulate driver handling risk conflicts via virtual CAN frames
  To verify that the VHAL correctly flags dangerous driver conditions

  Scenario: Driver attempts to drive away with Electronic Parking Brake engaged
    Given the Android Automotive emulator is active and responsive
    When the CAN simulator engages the Electronic Parking Brake
    And the driver attempts to shift the gear selection to DRIVE
    Then the CarService middleware must flag an active safety hazard conflict
