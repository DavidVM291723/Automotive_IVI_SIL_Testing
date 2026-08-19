# ==============================================================================
# AUTOMOTIVE VHAL ORCHESTRATOR & TEST RUNNER
# ==============================================================================
Clear-Host
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "      AUTOMOTIVE VHAL REGRESSION ORCHESTRATOR     " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Write-Host "Select execution mode:" -ForegroundColor Yellow
Write-Host "1) Run Traditional Unittest Suite (10 Isolated Modules)"
Write-Host "2) Run Advanced BDD Gherkin Suite (Behave Engine)"
Write-Host "3) Run Full Comprehensive Regression (Unittest + BDD)"
$Choice = Read-Host "`nEnter choice (1-3)"

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

# --- FUNCTION: RUN UNITTEST SUITE ---
function Run-UnittestSuite {
    Write-Host "`n==================================================" -ForegroundColor Cyan
    Write-Host " STARTING TRADITIONAL AUTOMOTIVE UNITTEST SUITE   " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    
    foreach ($Test in $TestCases) {
        $SuiteName = ($Test -split "/")[0]
        Write-Host "`n[ORCHESTRATOR] Target Suite: $SuiteName" -ForegroundColor Yellow
        
        # Dynamically mutate the docker-compose command
        $Content = Get-Content $ComposeFile
        $NewContent = $Content | ForEach-Object {
            if ($_ -match "command:") { "    command: python -m unittest $Test" } else { $_ }
        }
        Set-Content $ComposeFile $NewContent

        Write-Host " -> Spawning isolated container..." -ForegroundColor Gray
        docker compose up --build --exit-code-from can-simulator

        if ($LASTEXITCODE -ne 0) {
            Write-Host " -> [FAILED] Suite $SuiteName returned errors." -ForegroundColor Red
        } else {
            Write-Host " -> [PASSED] Suite $SuiteName completed clean." -ForegroundColor Green
        }
        Start-Sleep -Seconds 2
    }
}

# --- FUNCTION: RUN BDD SUITE ---
function Run-BddSuite {
    Write-Host "`n==================================================" -ForegroundColor Cyan
    Write-Host " STARTING ADVANCED BDD GHERKIN SUITE (BEHAVE)      " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    
    # Mutate docker-compose command to run the whole behave framework
    $Content = Get-Content $ComposeFile
    $NewContent = $Content | ForEach-Object {
        if ($_ -match "command:") { "    command: behave" } else { $_ }
    }
    Set-Content $ComposeFile $NewContent

    Write-Host " -> Spawning isolated BDD execution container..." -ForegroundColor Gray
    docker compose up --build --exit-code-from can-simulator

    if ($LASTEXITCODE -ne 0) {
        Write-Host " -> [FAILED] BDD Regression Suite returned errors." -ForegroundColor Red
    } else {
        Write-Host " -> [PASSED] BDD Regression Suite completed clean." -ForegroundColor Green
    }
}

# --- EXECUTION FLOW ORCHESTRATION ---
if ($Choice -eq "1") {
    Run-UnittestSuite
} elseif ($Choice -eq "2") {
    Run-BddSuite
} elseif ($Choice -eq "3") {
    Run-UnittestSuite
    Start-Sleep -Seconds 3
    Run-BddSuite
} else {
    Write-Host "[ERROR] Invalid option selected. Aborting orchestration." -ForegroundColor Red
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host " GLOBAL AUTOMOTIVE EVALUATION COMPLETED           " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
