Feature: Telematics and Cellular Call Signaling
  As a Baseband Network Validation Engineer
  I want to inject incoming call cellular events into the TCU modem
  To verify that the HMI prioritizes emergency or inbound layout windows

  Scenario: Deploy dialer interface over active foreground layer
    Given the Android Automotive emulator is active and responsive
    When an inbound cellular call event is registered from sender "+15551234567"
    Then the Android Automotive HMI must push the native dialer app to the foreground
