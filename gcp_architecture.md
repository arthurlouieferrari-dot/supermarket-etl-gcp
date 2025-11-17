## 🏗️ GCP Architecture Diagram

```mermaid
flowchart LR
    CS[Cloud Scheduler<br/>Cron Trigger]
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

    %% Force scaling notes to bottom by linking BI -> Scale (invisibly)
    BI -.-> Scale

    %% Strategy Notes (Not connected to graph)
    subgraph Scale [Scaling Strategy]
        A["Phase 1: Initial Lift & Shift<br/>• Pandas in Cloud Run<br/>(current implementation)"]
        B["Phase 2 (if required): Scale in Warehouse<br/>• Transformations in BigQuery SQL"]
        C["Phase 3 (if required): High Volume ETL<br/>• Dataflow / Dataproc for big/streaming jobs"]
    end
```
