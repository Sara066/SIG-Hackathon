KubeSentinel: AI-Powered Autonomous Healing- Docker Prototype
Predicts container failures before they happen, heals them autonomously, and provides a clear audit trail.

What it does: 
Continuous Monitoring: Scrapes live container metrics every 2 seconds via Prometheus. 
AI-Powered Detection: Identifies anomalies using a trained Isolation Forest model.
Proactive Healing: Acts autonomously to restart or redeploy containers when anomalies are detected.
Human-Readable Reasoning: Instead of just saying "Error," the system logs: “Memory usage (5.4MB) contributed +0.82 to the anomaly score, exceeding the safe baseline.”
Audit Transparency: Logs all actions to a persistent, plain-English audit log for human review.

Workflow: 
Prometheus + Node Exporter
↓ 
Metric Ingestion (Docker SDK + Python)
↓ 
Isolation Forest (Anomaly Scoring)
↓ 
Decision Logic (Healer Trigger)
↓
Autonomous Recovery (Restart/Redeploy)
↓
Persistent Audit Log (Action History)
↓
Generates Human Readable audit entry using SHAP ( Explainable AI)


Tech Stack: Orchestration- Docker + Docker Compose 
AI Model-Isolation Forest (scikit-learn)
Telemetry- Docker SDK for Python
Monitoring- Prometheus + Node Exporter
Data Science- Pandas + NumPy
Pre-requisites: Docker Desktop and installed Python 3.12

Road to the Final: Kubernetes Scaling This prototype intentionally uses Docker Compose to meet the 20-30% working prototype requirement for the screening round while
maintaining a low resource footprint. For the Final Offline Round at VIT Pune, the solution will be scaled to a Production-Grade Stack: Kubernetes Native: Migration from
Docker SDK to the Kubernetes Python Client to manage Pods and Deployments across clusters. 


Team
Reality Spectra — VIT Pune
CodeStorm Hackathon · Revdau Industries
@sig_realityspectra
