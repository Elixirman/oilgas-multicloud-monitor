# Group 9 Capstone: Multi-Cloud Oil & Gas Pipeline Monitoring Platform

## Overview
A simulated field site on **Azure** sends pipeline sensor data over a
private **IPsec VPN** to **AWS**, where a Kubernetes app stores and
displays it on a public dashboard.

- **Field (Azure):** Linux VM running a Dockerized sensor app
- **Link:** AWS VPC <-> Azure VNet, IPsec site-to-site VPN
- **HQ (AWS):** EKS cluster running API, database, dashboard
- **Edge:** AWS ALB + nip.io + cert-manager (free HTTPS, no domain)
- **Build:** console first, then Terraform (proves reproducibility)

See `docs/` for the full project plan and architecture diagram.

## Repo Structure
```
aws/            AWS Terraform
azure/          Azure Terraform
vpn/            VPN Terraform
app/

  sensor/       Sensor simulator (Dockerfile + script)
  api/          API service
  dashboard/    Dashboard service
k8s/            Kubernetes manifests
.github/workflows/   CI/CD pipelines
docs/           Diagrams, screenshots, project plan
```

## Workflow
1. Pick up an Issue (labeled by phase: network, vpn, app, k8s, edge)
2. Branch: `<name>/<phase>-<short-task>`
3. Commit: `[phase] short description`
4. Open a PR, link the Issue (`Closes #<number>`)
5. Get at least 1 review before merging to `main`

## Team
See `CONTRIBUTORS.md`.













## Environment Variables
 
| Variable | Used By | Purpose | Set In |
|---|---|---|---|
| POSTGRES_USER | api, database | DB login username | k8s/db-secret.yaml |
| POSTGRES_PASSWORD | api, database | DB login password | k8s/db-secret.yaml |
| POSTGRES_DB | api, database | database name | k8s/db-secret.yaml |
| DB_HOST | api | database Service name/address | k8s/api.yaml env |
| API_URL | dashboard-app, azure-field | address of the API | k8s/dashboard.yaml env, sensor env |
| DOCKERHUB_USERNAME | GitHub Actions | Docker Hub login | GitHub Secrets |
| DOCKERHUB_TOKEN | GitHub Actions | Docker Hub auth token | GitHub Secrets 
## Setup Instructions
 
Prerequisites:
- git
- Python 3.11+
- Docker
- aws-cli, az-cli
- kubectl
- terraform
 
Clone the repo:
```
git clone https://github.com/Elixirman/oilgas-multicloud-monitor.git
cd oilgas-multicloud-monitor
```
 
Run each app locally (3 terminals):
```
cd api && pip install -r requirements.txt && python3 app.py
cd azure-field && pip install -r requirements.txt && python3 sensor_app.py
cd dashboard-app && pip install -r requirements.txt && python3 app.py
```
Open http://localhost:5000
## Deployment Instructions
 
Phase 1 - Networks: build AWS VPC and Azure VNet (console or Terraform in aws/ and azure/)
Phase 2 - VPN: connect the two networks with IPsec site-to-site VPN
Phase 3 - Containers: build and push Docker images (see .github/workflows/ci-cd.yml)
Phase 4 - Kubernetes: apply manifests in order
```
kubectl apply -f k8s/db-secret.yaml
kubectl apply -f k8s/database.yaml
kubectl apply -f k8s/api.yaml
kubectl apply -f k8s/dashboard.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```
Phase 5 - Edge: confirm ALB is provisioned, get its hostname, verify the nip.io URL and HTTPS cert
Phase 6 - Verify: generate a reading on the field VM, confirm it appears on the public dashboard
## Troubleshooting
 
**VPN tunnel shows Down**
- Confirm the pre-shared key matches exactly on both sides
- Confirm IPsec settings (IKE version, encryption) match on both gateways
- Check route tables include the peer's CIDR
 
**Pod stuck in CrashLoopBackOff**
- Run: kubectl logs <pod-name>
- Check the /health endpoint path and port match the probe config
- Confirm environment variables are set (kubectl describe pod <pod-name>)
 
**ALB returns 502**
- Confirm the dashboard pod is Ready: kubectl get pods
- Check the Service selector matches the pod labels
- Confirm the target group health check path is /health
 
**cert-manager not issuing a certificate**
- Run: kubectl describe certificate <name>
- Confirm the nip.io hostname resolves to the ALB's real IP
- Check cert-manager logs: kubectl logs -n cert-manager deploy/cert-manager
 
**CI/CD pipeline failing on build-and-push**
- Confirm DOCKERHUB_USERNAME and DOCKERHUB_TOKEN are set in repo Secrets
- Confirm each app folder has a Dockerfile
 
**Database connection refused**
- Confirm DB_HOST matches the database Service name ("database") once in Kubernetes
- Confirm db-secret.yaml values are correct and applied before the api/database deployments
See `docs/architecture-reference.docx` for the full architecture diagram, traffic flow, and resource breakdown.
