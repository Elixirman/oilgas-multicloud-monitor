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
