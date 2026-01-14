**CommoTrade: Cloud-Native Financial Signal Engine**

\!\[Status\](https://img.shields.io/badge/Status-Operational-success)  
\!\[AWS\](https://img.shields.io/badge/AWS-EKS-orange)  
\!\[Terraform\](https://img.shields.io/badge/IaC-Terraform-purple)  
\!\[Kubernetes\](https://img.shields.io/badge/K8s-v1.30-blue)

\*\*CommoTrade\*\* is a resilient, cloud-native microservice designed to simulate a Bloomberg-style financial data feed. It ingests real-time market data (Crude Oil, Gold), applies algorithmic trading logic (BUY/SELL signals), and exposes metrics via a JSON API and Prometheus endpoints.

Built on \*\*AWS EKS\*\* using \*\*Terraform\*\*, this project demonstrates a production-grade DevSecOps pipeline handling infrastructure-as-code, container orchestration, and automated recovery from critical state failures.

\---

**\#\# 🏗 Architecture**

The system follows a 3-tier cloud architecture deployed in the \`ap-southeast-1\` (Singapore) region:

1\.  \*\*Infrastructure Layer (Terraform):\*\*  
    \* \*\*VPC:\*\* Custom VPC with public/private subnets and NAT Gateways.  
    \* \*\*Compute:\*\* AWS EKS Cluster (v1.30) with Managed Node Groups (t3.medium).  
    \* \*\*Security:\*\* IAM Roles for Service Accounts (IRSA) and minimal-privilege Security Groups.

2\.  \*\*Application Layer (Kubernetes):\*\*  
    \* \*\*Deployment:\*\* Python Flask microservice (ReplicaSet for high availability).  
    \* \*\*Service:\*\* Network Load Balancer (NLB) for external access.  
    \* \*\*Container:\*\* Dockerized Python 3.10 runtime stored in AWS ECR.

3\.  \*\*Data Layer:\*\*  
    \* \*\*Feed:\*\* Real-time integration with Yahoo Finance (\`yfinance\`).  
    \* \*\*Logic:\*\* Volatility-based signal generation (Threshold \> 0.5% deviation).

\---

**\#\# 🛠 Tech Stack**

\* \*\*Cloud Provider:\*\* AWS (EKS, ECR, VPC, IAM, ELB)  
\* \*\*IaC:\*\* Terraform (State management, Module-based architecture)  
\* \*\*Orchestration:\*\* Kubernetes 1.30 (\`kubectl\`)  
\* \*\*Containerization:\*\* Docker (Multi-stage builds, Python 3.10-slim)  
\* \*\*Language:\*\* Python (Flask, Prometheus Client, Pandas)

\---

**\#\# 🚀 Key Features**

\* \*\*Real-Time Signal Processing:\*\*  
    \* Streams live ticks for \`CL=F\` (Crude Oil) and \`GC=F\` (Gold).  
    \* Calculates % change from previous close.  
    \* Generates signals: \`BUY\` (Drop \> 0.5%), \`SELL\` (Rise \> 0.5%), \`HOLD\`.  
\* \*\*Observability:\*\*  
    \* Exposes \`/terminal\` endpoint for frontend consumption.  
    \* Exports Prometheus metrics on port \`8000\` for Grafana scraping (\`trade\_signal\`, \`data\_latency\_ms\`).  
\* \*\*Self-Healing:\*\*  
    \* Kubernetes Liveness Probes ensure zero downtime during crashes.  
    \* Rolling Updates strategy (\`v2\` deployment) used for patching.

\---

**\#\# 🔧 Engineering Challenges Solved**

\#\#\# 1\. The "Split-Brain" Terraform Incident  
\*\*Situation:\*\* During the initial provision, the local machine crashed, corrupting the Terraform state file (\`terraform.tfstate\`) while the AWS EKS cluster was partially created.  
\*\*Resolution:\*\*  
\* Avoided \`terraform destroy\` to prevent production downtime.  
\* Performed a \*\*State Import\*\* (\`terraform import\`) to manually reconcile the existing AWS Cluster ID with the Terraform configuration.  
\* Aligned version tags to match the live infrastructure (downgraded config from 1.32 to 1.30).

\#\#\# 2\. The Python 3.10 Upgrade Strategy  
\*\*Situation:\*\* The application entered a \`CrashLoopBackOff\` upon deployment.  
\*\*Root Cause:\*\* The \`yfinance\` library introduced modern Python syntax (\`|\` operator) incompatible with the base image (\`python:3.9\`).  
\*\*Resolution:\*\*  
\* Refactored \`Dockerfile\` to use \`python:3.10-slim\`.  
\* Executed a \*\*Rolling Update\*\* by tagging a new image version (\`v2\`) to bypass Kubernetes caching mechanisms (\`latest\` tag trap).  
\* Result: 100% pod health with zero service interruption.

\---

**\#\# 💻 Usage**

\#\#\# Prerequisites  
\* AWS CLI configured  
\* Terraform installed  
\* Docker Desktop running

**\#\#\# Deployment**  
1\.  \*\*Provision Infrastructure:\*\*  
    \`\`\`bash  
    cd terraform  
    terraform init  
    terraform apply \--auto-approve  
    \`\`\`

2\.  \*\*Build & Ship Code:\*\*  
    \`\`\`bash  
    cd ../commotrade  
    docker build \-t commotrade:v2 .  
    \# Login & Push to AWS ECR  
    docker push \<aws\_account\_id\>\[.dkr.ecr.ap-southeast-1.amazonaws.com/commotrade:v2\](https://.dkr.ecr.ap-southeast-1.amazonaws.com/commotrade:v2)  
    \`\`\`

3\.  \*\*Deploy to Kubernetes:\*\*  
    \`\`\`bash  
    kubectl apply \-f k8s/  
    kubectl set image deployment/commotrade-app commotrade=\<ecr\_repo\>:v2  
    \`\`\`

4\.  \*\*Access Terminal:\*\*  
    \`\`\`bash  
    kubectl get service commotrade-service  
    \# Visit EXTERNAL-IP/terminal  
    \`\`\`

\---

\#\# **📸 Proof of Concept**  
![][image1]

\---  
\*Created by \[Muhamed Imraan(Roger)\] \- 2026\*  


[image1]: <data:image/png;base64,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eUVdErTcsm6d5DW41TcONXPG1ySfKXebsR6XE4AaGp1bUh31m+IzY/FjF2woEf4tvaopfixFVBcJeLas3GZf6rbtzBktl3dbbKnbkf1bn91b/91bevUwp+7u7cM6CMot/M5wVyWBFAAA5Auu0erMpiXPBmr5uiI3QEx7tDHzlG+k2nJGDgAAGDtU0GqWp5q9X8EzbcpcDI+UhNGl09MHeAIAgNbZoYIWAABAR0LQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCAELQAAgIIQtAAAAApC0AIAACgIQQsAAKAgBC0AAICCELQAAAAKQtACAAAoCEELAACgIAQtAACAghC0AAAACkLQAgAAKAhBCwAAoCD/C+7NsGOugL5yAAAAAElFTkSuQmCC>