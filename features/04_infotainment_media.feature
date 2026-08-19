Feature: Infotainment and Media Controls
  As an In-Vehicle Infotainment (IVI) Systems Auditor
  I want to trigger steering wheel button interrupts over the CAN bus
  To verify that the Android Audio subsystem scales output parameters correctly

  Scenario: Orchestrate media stream volume and track skipping
    Given the Android Automotive emulator is active and responsive
    When the driver presses the volume UP steering wheel accessory button
    Then the CarService audio manager must scale the master volume group to 60 percent
    When the driver presses the NEXT TRACK accessory button interrupt
    Then the Android multimedia layer must process a keyevent 87 media interrupt
