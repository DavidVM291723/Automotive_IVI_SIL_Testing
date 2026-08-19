Feature: Driver Distraction and UX Restrictions
  As a Road Safety Systems Auditor
  I want to trigger vehicle acceleration variables over the virtual CAN bus
  To verify that Android Automotive enforces app lockdown constraints in motion

  Scenario: Enforce and release UXR applications based on speed telemetry
    Given the Android Automotive emulator is active and responsive
    When the vehicle transmission shifts to DRIVE and acceleration scales to 85 km/h
    Then the VHAL UX Restrictions must be ENFORCED to block non-optimized apps
    When the vehicle decelerates to 0 km/h and shifts back to PARKING
    Then the VHAL UX Restrictions must be DISABLED to unlock the HMI screen
