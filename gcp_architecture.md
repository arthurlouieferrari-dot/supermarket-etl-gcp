## 🏗️ GCP Architecture Diagram

```mermaid
flowchart LR
    CS[Cloud Scheduler<br/>Cron Trigger
    CR[Cloud Run Job<br/>Python ETL]
    SM[Secret Manager]
    RAW[Cloud Storage<br/>Raw Kaggle Files]
    PROC[Cloud Storage<br/>Processed Files]
    BQ[BigQuery<br/>Dim + Fact Tables]
    BQREP[BigQuery Scheduled Query<br/>Analytical Report]
    BI[Looker Studio / BI Tools]

    CS --> CR
    SM --> CR
    CR --> RAW
    CR --> PROC
    CR --> BQ
    BQ --> BQREP
    BQREP --> BI
```
