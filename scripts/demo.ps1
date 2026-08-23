$ErrorActionPreference = "Stop"

$baseUrl = "http://localhost:8000"
$headers = @{ "Content-Type" = "application/json" }
$userId = "demo_yussef_v3"

Write-Host "1. Checking FastAPI and FalkorDB..."
Invoke-RestMethod -Method Get -Uri "$baseUrl/health" | ConvertTo-Json
Invoke-RestMethod -Method Get -Uri "$baseUrl/ready" | ConvertTo-Json

Write-Host "2. Adding an invented memory episode..."
$memoryBody = @{
    user_id = $userId
    content = "Yussef practica natacion cinco dias por semana."
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/memory/episodes" `
    -Headers $headers `
    -Body $memoryBody | ConvertTo-Json -Depth 6

Write-Host "3. Searching the temporal graph..."
$searchBody = @{
    user_id = $userId
    query = "Que deporte practica el usuario?"
    limit = 5
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/memory/search" `
    -Headers $headers `
    -Body $searchBody | ConvertTo-Json -Depth 6

Write-Host "4. Asking the memory-aware chatbot..."
$chatBody = @{
    user_id = $userId
    message = "Recomiendame una actividad relacionada con lo que sabes de mi."
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/chat" `
    -Headers $headers `
    -Body $chatBody | ConvertTo-Json -Depth 6

Write-Host "Demo completed. Open http://localhost:3000 to inspect graphiti_memory_$userId."
