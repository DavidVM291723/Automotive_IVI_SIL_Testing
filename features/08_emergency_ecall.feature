Feature: Automated Emergency eCall System
  As a Regulatory Safety Compliance Auditor
  I want to simulate passive crash sensor triggers over the vehicle network
  To verify that Android Automotive preempts the HMI and routes an automated SOS call

  Scenario: Prioritize critical safety dialer over active foreground contexts
    Given the Android Automotive emulator is active and responsive
    When a high-impact crash frame triggers the automated eCall SOS sensor
    Then the HMI layer must immediately force deploy the emergency routing layout
