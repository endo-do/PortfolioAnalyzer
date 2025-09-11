# Test script for Docker setup verification
# This script helps verify that the Docker setup works correctly

Write-Host "Testing Docker Setup for Portfolio Analyzer" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "   Please copy env.example to .env and configure your database credentials" -ForegroundColor Yellow
    exit 1
}

Write-Host "SUCCESS: .env file found" -ForegroundColor Green

# Check if required environment variables are set
$envContent = Get-Content ".env"
$requiredVars = @("DB_ROOT_PASSWORD", "DB_USER", "DB_PASSWORD", "DB_NAME", "SECRET_KEY")
$missingVars = @()

foreach ($var in $requiredVars) {
    $found = $false
    foreach ($line in $envContent) {
        if ($line -match "^$var=" -and $line -notmatch "^$var=$") {
            $found = $true
            break
        }
    }
    if (-not $found) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "ERROR: Missing required environment variables:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "   - $var" -ForegroundColor Yellow
    }
    Write-Host "   Please update your .env file with the required values" -ForegroundColor Yellow
    exit 1
}

Write-Host "SUCCESS: All required environment variables are set" -ForegroundColor Green

# Clean up any existing containers
Write-Host "Cleaning up existing containers..." -ForegroundColor Yellow
docker-compose down -v 2>$null

# Build and start the containers
Write-Host "Building and starting containers..." -ForegroundColor Yellow
if (docker-compose up --build -d) {
    Write-Host "SUCCESS: Containers started successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to start containers" -ForegroundColor Red
    exit 1
}

# Wait for services to be healthy
Write-Host "Waiting for services to be healthy..." -ForegroundColor Yellow
$timeout = 300  # 5 minutes
$elapsed = 0

while ($elapsed -lt $timeout) {
    $status = docker-compose ps
    if ($status -match "healthy") {
        Write-Host "SUCCESS: Services are healthy" -ForegroundColor Green
        break
    }
    
    Write-Host "   Still waiting... ($elapsed s elapsed)" -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    $elapsed += 10
}

if ($elapsed -ge $timeout) {
    Write-Host "ERROR: Services did not become healthy within $timeout seconds" -ForegroundColor Red
    Write-Host "Container status:" -ForegroundColor Yellow
    docker-compose ps
    Write-Host "Container logs:" -ForegroundColor Yellow
    docker-compose logs --tail=50
    exit 1
}

# Test web application
Write-Host "Testing web application..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS: Web application is responding" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Web application returned status code: $($response.StatusCode)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: Web application is not responding" -ForegroundColor Red
    Write-Host "Web container logs:" -ForegroundColor Yellow
    docker-compose logs web --tail=20
    exit 1
}

Write-Host ""
Write-Host "SUCCESS: Docker setup test completed successfully!" -ForegroundColor Green
Write-Host "Your application is available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Admin credentials:" -ForegroundColor Yellow
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: [from your .env ADMIN_PASSWORD]" -ForegroundColor White
Write-Host ""
Write-Host "To view logs: docker-compose logs -f" -ForegroundColor Cyan
Write-Host "To stop: docker-compose down" -ForegroundColor Cyan