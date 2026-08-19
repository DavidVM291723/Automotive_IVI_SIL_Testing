Feature: Voice Assistant Steering Wheel Control
  As an In-Cabin Experience Engineer
  I want to route push-to-talk steering wheel button interrupts over the CAN bus
  To verify that the system successfully wakes up the native speech assistant overlay

  Scenario: Invoke speech interaction window via hardware interrupt
    Given the Android Automotive emulator is active and responsive
    When the driver interacts with the steering wheel push-to-talk voice button
    Then the VoiceInteractionManagerService must deploy the active speech context window
