# ==============================================================================
# AUTOMOTIVE VHAL TEST SUITE ORCHESTRATOR (TEST RUNNER)
# ==============================================================================
Clear-Host
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " LAUNCHING GLOBAL AUTOMOTIVE VHAL TEST SUITE      " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# List of all test scripts to execute
$TestCases = @(
    "01_Cabin_Comfort_HVAC/test_hvac.py",
    "02_Driver_Distraction/test_distraction.py",
    "03_Vehicle_Status_Safety/test_safety.py",
    "04_Infotainment_Media/test_media.py",
    "05_Telematics_Calls/test_calls.py",
    "06_Engine_Diagnostics_DTC/test_diagnostics.py",
    "07_Vehicle_Location_GPS/test_location.py",
    "08_Emergency_eCall/test_ecall.py",
    "09_Voice_Assistant_Intent/test_assistant.py",
    "10_Vehicle_Network_Internet/test_network.py"
)

$ComposeFile = "docker-compose.yml"

foreach ($Test in $TestCases) {
    $SuiteName = ($Test -split "/")[0]
    Write-Host "`n[ORCHESTRATOR] Target Suite: $SuiteName" -ForegroundColor Yellow
    
    # Dynamically rewrite the command line inside the docker-compose file
    $Content = Get-Content $ComposeFile
    $NewContent = $Content | ForEach-Object {
        if ($_ -match "command:") {
            "    command: python -m unittest $Test"
        } else {
            $_
        }
    }
    Set-Content $ComposeFile $NewContent

    # Execute the Docker container for the current test case
    Write-Host " -> Spawning isolated container container..." -ForegroundColor Gray
    docker compose up --build --exit-code-from can-simulator

    if ($LASTEXITCODE -ne 0) {
        Write-Host " -> [FAILED] Suite $SuiteName returned errors." -ForegroundColor Red
    } else {
        Write-Host " -> [PASSED] Suite $SuiteName completed clean." -ForegroundColor Green
    }
    
    # Brief cooldown between hardware state shifts
    Start-Sleep -Seconds 2
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host " GLOBAL AUTOMOTIVE EVALUATION COMPLETED          " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
