# Despliega todo el sistema en Minikube con un solo comando.
# Uso (PowerShell, desde la carpeta del repo, con Docker Desktop abierto):
#     powershell -ExecutionPolicy Bypass -File .\scripts\desplegar.ps1
# Pide dos claves (no se muestran en pantalla) y crea el Secret "app-secrets".
# Se puede ejecutar varias veces: si el Secret ya existe, lo conserva.

function Fallar($mensaje) {
    Write-Host ""
    Write-Host "ERROR: $mensaje" -ForegroundColor Red
    exit 1
}

function Paso($texto) {
    Write-Host ""
    Write-Host "== $texto" -ForegroundColor Cyan
}

function LeerClave($texto) {
    while ($true) {
        $segura = Read-Host $texto -AsSecureString
        $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($segura)
        try { $clave = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
        finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
        if ($clave -match '^[A-Za-z0-9]{4,}$') { return $clave }
        Write-Host "Use solo letras y numeros, minimo 4 caracteres." -ForegroundColor Yellow
    }
}

# Trabajar siempre desde la raiz del repo (la carpeta que contiene k8s/)
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path "k8s\kustomization.yaml")) { Fallar "No encuentro k8s\kustomization.yaml. Ejecute el script dentro del repo entrega2." }

Paso "1/6 Revisando herramientas"
foreach ($programa in "docker", "minikube", "kubectl") {
    if (-not (Get-Command $programa -ErrorAction SilentlyContinue)) { Fallar "Falta instalar '$programa'." }
}
docker info *> $null
if ($LASTEXITCODE -ne 0) { Fallar "Docker no responde. Abra Docker Desktop, espere a que cargue y repita." }

Paso "2/6 Iniciando Minikube (puede tardar unos minutos la primera vez)"
minikube start
if ($LASTEXITCODE -ne 0) { Fallar "minikube start fallo. Revise el mensaje de arriba." }

Paso "3/6 Creando namespace y Secret"
kubectl apply -f k8s/00-namespace.yaml
if ($LASTEXITCODE -ne 0) { Fallar "No se pudo crear el namespace." }

kubectl get secret app-secrets -n ahorro *> $null
if ($LASTEXITCODE -eq 0) {
    Write-Host "El Secret app-secrets ya existe: se conserva."
} else {
    Write-Host "Elija dos claves cualquiera para la base de datos y el administrador."
    $clavePg = LeerClave "Clave de la base de datos (PG_PASSWORD)"
    $claveAdmin = LeerClave "Clave del administrador (ADMIN_PASSWORD)"
    kubectl create secret generic app-secrets -n ahorro "--from-literal=PG_PASSWORD=$clavePg" "--from-literal=ADMIN_PASSWORD=$claveAdmin"
    if ($LASTEXITCODE -ne 0) { Fallar "No se pudo crear el Secret." }
}

Paso "4/6 Aplicando los manifiestos"
# El Job de seeding no se puede modificar una vez creado: se borra y se vuelve a crear.
kubectl delete job seed -n ahorro --ignore-not-found
kubectl apply -k k8s/
if ($LASTEXITCODE -ne 0) { Fallar "kubectl apply -k k8s/ fallo." }

Paso "5/6 Esperando a que todo este listo"
kubectl rollout status statefulset/db -n ahorro --timeout=300s
if ($LASTEXITCODE -ne 0) { Fallar "La base de datos no arranco. Pruebe: kubectl describe pod db-0 -n ahorro" }
kubectl wait --for=condition=complete job/seed -n ahorro --timeout=300s
if ($LASTEXITCODE -ne 0) { Fallar "El seeding no termino. Pruebe: kubectl logs job/seed -n ahorro" }
kubectl rollout status deployment/backend -n ahorro --timeout=300s
if ($LASTEXITCODE -ne 0) { Fallar "El backend no arranco. Pruebe: kubectl logs deploy/backend -n ahorro" }
kubectl rollout status deployment/frontend -n ahorro --timeout=300s
if ($LASTEXITCODE -ne 0) { Fallar "El frontend no arranco. Pruebe: kubectl describe pod -l app=frontend -n ahorro" }

Paso "6/6 Estado final"
kubectl get pods -n ahorro
kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image

Write-Host ""
Write-Host "LISTO. Para abrir la pagina corra este comando y DEJE LA VENTANA ABIERTA:" -ForegroundColor Green
Write-Host "    minikube service frontend -n ahorro --url"
Write-Host "Luego abra en el navegador la direccion que imprime."
