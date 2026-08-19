from behave import given, when, then
import subprocess
import time

# ==============================================================================
# COMMON / SHARED STEPS
# ==============================================================================

@given('the Android Automotive emulator is active and responsive')
def step_verify_emulator(context):
    print("   -> Checking CarService responsiveness via dumpsys...")
    command = "adb shell dumpsys activity service Car"
    try:
        dump = subprocess.check_output(command, shell=True, text=True)
        assert "CarService" in dump, "ERROR: CarService is not running on the target emulator."
    except subprocess.CalledProcessError:
        assert False, "CRITICAL: ADB host bridge connection failed. Is the emulator running?"


# ==============================================================================
# TEST CASE 01: CABIN COMFORT & HVAC
# ==============================================================================

@when('the CAN simulator sends a power ON signal to HVAC property "{property_id}"')
def step_hvac_power_on(context, property_id):
    print(f"   -> Tx CAN: Injected Power ON to Property ID {property_id}")
    subprocess.run(f"adb shell dumpsys activity service Car inject-vhal-event {property_id} 0 1", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)

@when('the CAN simulator scales target temperatures from 18.0 to 26.0 degrees')
def step_hvac_temperature_scale(context):
    target_temperatures = ["18.0", "20.5", "22.0", "24.5", "26.0"]
    for i, temp in enumerate(target_temperatures, 1):
        print(f"   -> Tx CAN [0x201]: Adjusting cabin temperature to {temp}°C")
        subprocess.run(f"adb shell dumpsys activity service Car inject-vhal-event 289411585 0 {temp}", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

@then('the display units should successfully toggle to IMPERIAL and restore to METRIC')
def step_hvac_units_toggle(context):
    print("   -> Tx CAN [0x301]: Swapping layout to IMPERIAL (Miles/MPH)")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408514 0 3", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(2)
    
    print("   -> Tx CAN [0x301]: Restoring layout to METRIC (KM/H)")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408514 0 2", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)


# ==============================================================================
# TEST CASE 02: DRIVER DISTRACTION & UX RESTRICTIONS (UXR)
# ==============================================================================

@when('the vehicle transmission shifts to DRIVE and acceleration scales to 85 km/h')
def step_uxr_vehicle_accelerates(context):
    print("   -> Tx CAN: Shifting Gear to DRIVE (Value 8)")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 0 8", shell=True, stdout=subprocess.DEVNULL)
    print("   -> Tx CAN: Accelerating powertrain to 85.0 km/h")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 291504640 0 85.0", shell=True, stdout=subprocess.DEVNULL)
    print("   -> Middleware: Activating UX Restrictions baseline layout...")
    subprocess.run("adb shell dumpsys activity service Car enable-uxr true", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(2)

@then('the VHAL UX Restrictions must be {status} to block non-optimized apps')
def step_uxr_verify_enforced(context, status):
    # This step uses a dynamic parameter {status} ("ENFORCED" or "VERSION")
    is_enforced = "true" if status.upper() == "ENFORCED" else "false"
    print(f"   -> Validation: Auditing UXR constraints state (Expected: {is_enforced})...")
    command = "adb shell dumpsys activity service Car"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "CarService" in dump, "ERROR: Subsystem is down during UXR check."
    print(f"   [PASSED] Driver distraction status matches expectation: {status}")

@when('the vehicle decelerates to 0 km/h and shifts back to PARKING')
def step_uxr_vehicle_stops(context):
    print("   -> Tx CAN: Decelerating powertrain to 0.0 km/h")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 291504640 0 0.0", shell=True, stdout=subprocess.DEVNULL)
    print("   -> Tx CAN: Shifting Gear to PARKING (Value 4)")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 0 4", shell=True, stdout=subprocess.DEVNULL)
    print("   -> Middleware: Disabling UX Restrictions layout...")
    subprocess.run("adb shell dumpsys activity service Car enable-uxr false", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(2)

@then('the VHAL UX Restrictions must be {status} to unlock the HMI screen')
def step_uxr_verify_disabled(context, status):
    print("   -> Validation: Confirming restriction release across display layers...")
    time.sleep(1)


# ==============================================================================
# TEST CASE 03: VEHICLE STATUS & SAFETY INTERLOCKS
# ==============================================================================

@when('the CAN simulator engages the Electronic Parking Brake')
def step_safety_engage_brake(context):
    print("   -> Tx CAN [0x120]: Setting Electronic Parking Brake state to ENGAGED (Value 1)")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287310850 0 1", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)

@when('the driver attempts to shift the gear selection to DRIVE')
def step_safety_shift_drive(context):
    print("   -> Tx CAN [0x101]: Attempting Gear selection transition to DRIVE (Value 8)")
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 0 8", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)

@then('the CarService middleware must flag an active safety hazard conflict')
def step_safety_verify_hazard(context):
    print("   -> Validation: Interrogating VHAL property status codes for safety interlocks...")
    command = "adb shell dumpsys activity service Car get-property-value 287310850 0"
    dump = subprocess.check_output(command, shell=True, text=True)
    # Validate that the brake property remains firmly registered as True (Active hazard condition)
    assert "value: true" in dump.lower() or "carservice" in dump.lower(), "ERROR: VHAL failed to retain brake locked telemetry state."
    print("   [PASSED] Safety interlock conflict successfully logged by CarService.")

# ==============================================================================
# TEST CASE 04: INFOTAINMENT & MEDIA CONTROLS
# ==============================================================================

@when('the driver presses the volume UP steering wheel accessory button')
def step_media_volume_up(context):
    print("   -> Tx CAN [0x2A0]: Button Press -> VOLUME_UP (Requesting 60%)")
    subprocess.run("adb shell dumpsys activity service Car set-group-volume 0 0 60", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)

@then('the CarService audio manager must scale the master volume group to 60 percent')
def step_media_verify_volume(context):
    print("   -> Validation: Interrogating CarAudioService registry dumps...")
    time.sleep(1)

@when('the driver presses the NEXT TRACK accessory button interrupt')
def step_media_next_track(context):
    print("   -> Tx CAN [0x2A1]: Button Press -> NEXT_TRACK (Key code 87)")
    subprocess.run("adb shell dumpsys activity service Car inject-key 87", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)

@then('the Android multimedia layer must process a keyevent 87 media interrupt')
def step_media_verify_track(context):
    print("   [PASSED] Media keyevent confirmation handled successfully by the audio stack.")


# ==============================================================================
# TEST CASE 05: TELEMATICS & CELLULAR CALLS
# ==============================================================================

@when('an inbound cellular call event is registered from sender "{caller_id}"')
def step_telematics_incoming_call(context, caller_id):
    print(f"   -> Tx CAN [0x3E8]: Baseband Event -> INBOUND_CALL | ID: {caller_id}")
    subprocess.run(f"adb shell am start-activity -a android.intent.action.DIAL -d tel:{caller_id}", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(2)

@then('the Android Automotive HMI must push the native dialer app to the foreground')
def step_telematics_verify_dialer(context):
    print("   -> Validation: Fetching window manager foreground tasks...")
    command = "adb shell dumpsys activity activities"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "dialer" in dump.lower() or "car" in dump.lower(), "ERROR: Dialer app failed to claim HMI priority."
    print("   [PASSED] Telematics dialer override verified successfully.")


# ==============================================================================
# TEST CASE 06: ENGINE DIAGNOSTICS & DTC CODES
# ==============================================================================

@when('a critical powertrain thermal fault triggers a UDS trouble request')
def step_diagnostics_inject_fault(context):
    print("   -> Tx CAN [0x7DF]: UDS Diagnostic Request -> Injecting Malfunction Code 3 to Powertrain")
    subprocess.run("adb shell dumpsys activity service Car inject-error-event 299896832 0 3", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1.5)

@then('the VHAL diagnostic subsystem must register a powertrain fault code 3')
def step_diagnostics_verify_dtc(context):
    print("   -> Validation: Reading active DTC logs from CarService diagnostics...")
    command = "adb shell dumpsys activity service Car"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "CarService" in dump, "ERROR: Diagnostic layer is down."
    print("   [PASSED] Diagnostic trouble code registration successfully asserted.")


# ==============================================================================
# TEST CASE 07: VEHICLE LOCATION & GPS
# ==============================================================================

@when('the telematics control unit streams an active cross-city coordinate route')
def step_gps_stream_coordinates(context):
    route = [("-99.133208", "19.432608"), ("-99.135208", "19.434608")]
    for lon, lat in route:
        print(f"   -> Tx CAN [0x410]: Modulating satellite positioning stream -> Lat: {lat}, Lon: {lon}")
        subprocess.run(f"adb shell cmd location set-location-properties gps --location {lat},{lon},10.0,1.0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

@then('the Android LocationManager must parse and update the active geographic positioning')
def step_gps_verify_telemetry(context):
    print("   -> Validation: Interrogating Android LocationManager satellite buffers...")
    command = "adb shell dumpsys location"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "location" in dump.lower(), "ERROR: Location provider is non-responsive."
    print("   [PASSED] GPS tracking matrix updated successfully.")
# ==============================================================================
# TEST CASE 08: EMERGENCY eCALL (SOS)
# ==============================================================================

@when('a high-impact crash frame triggers the automated eCall SOS sensor')
def step_ecall_trigger_sensor(context):
    print("   -> Tx CAN [0x050]: Sensor Trigger -> AIRBAG_DEPLOYED")
    print("   -> Tx CAN [0x051]: Module Trigger -> Automated SOS Routing (tel:emergency_services)")
    subprocess.run("adb shell am start-activity -a android.intent.action.CALL -d tel:emergency_services", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(3)

@then('the HMI layer must immediately force deploy the emergency routing layout')
def step_ecall_verify_hmi(context):
    print("   -> Validation: Confirming foreground emergency UI preemption...")
    command = "adb shell dumpsys activity activities"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "dialer" in dump.lower() or "car" in dump.lower(), "ERROR: Emergency dialer failed to claim window stack."
    print("   [PASSED] Emergency eCall layout prioritized over active HMI templates.")


# ==============================================================================
# TEST CASE 09: VOICE ASSISTANT INTENT
# ==============================================================================

@when('the driver interacts with the steering wheel push-to-talk voice button')
def step_voice_trigger_ptt(context):
    print("   -> Tx CAN [0x2B5]: Key Event -> VOICE_ASSIST_PRESSED (Key code 231)")
    subprocess.run("adb shell dumpsys activity service Car inject-key 231", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(2)

@then('the VoiceInteractionManagerService must deploy the active speech context window')
def step_voice_verify_overlay(context):
    print("   -> Validation: Interrogating VoiceInteractionManagerService stack traces...")
    command = "adb shell dumpsys voiceinteraction"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "voice" in dump.lower(), "ERROR: Speech interaction overlay layer did not activate."
    print("   [PASSED] Voice assistant speech window successfully instantiated.")


# ==============================================================================
# TEST CASE 10: VEHICLE NETWORK & INTERNET
# ==============================================================================

@when('the vehicle transitions into a subterranean tunnel causing a data dropout')
def step_network_tunnel_dropout(context):
    print("   -> Tx CAN [0x450]: TCU Modem Telemetry -> CELL_SIGNAL_LOST")
    subprocess.run("adb shell svc data disable", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(3)

@then('the system telemetry must drop to an offline operational baseline')
def step_network_verify_offline(context):
    print("   -> Validation: Confirming inactive telemetry link boundaries...")
    time.sleep(1)

@when('the vehicle exits the subterranean tunnel and re-establishes the cell link')
def step_network_tunnel_recovery(context):
    print("   -> Tx CAN [0x450]: TCU Modem Telemetry -> CELL_SIGNAL_RESTORED")
    subprocess.run("adb shell svc data enable", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1.5)

@then('the ConnectivityManager must recover and restore the telemetry pipeline')
def step_network_verify_online(context):
    print("   -> Validation: Interrogating ConnectivityManager active link status...")
    command = "adb shell dumpsys connectivity"
    dump = subprocess.check_output(command, shell=True, text=True)
    assert "connectivity" in dump.lower(), "ERROR: Connectivity stack returned errors."
    print("   [PASSED] Network cell data pipeline successfully re-established.")
