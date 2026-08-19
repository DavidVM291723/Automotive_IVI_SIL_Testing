Feature: Cabin Comfort and HVAC Telemetry
  As an Automotive Validation Engineer
  I want to inject climate and display signals into the VHAL
  To verify the Android CarService processes dashboard parameters properly

  Scenario: Linearly scale cabin temperature and toggle measurement units
    Given the Android Automotive emulator is active and responsive
    When the CAN simulator sends a power ON signal to HVAC property "287312384"
    And the CAN simulator scales target temperatures from 18.0 to 26.0 degrees
    Then the display units should successfully toggle to IMPERIAL and restore to METRIC
