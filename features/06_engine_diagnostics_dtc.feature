Feature: Engine Diagnostics and Trouble Code Logging
  As a Powertrain Diagnostics Architect
  I want to broadcast hardware malfunction signals over the UDS network
  To verify that the VHAL logs Diagnostic Trouble Codes (DTCs) under OBD2 rules

  Scenario: Log critical engine coolant malfunction state into the cluster
    Given the Android Automotive emulator is active and responsive
    When a critical powertrain thermal fault triggers a UDS trouble request
    Then the VHAL diagnostic subsystem must register a powertrain fault code 3
