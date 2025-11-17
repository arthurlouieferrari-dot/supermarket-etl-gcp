## 🏗️ GCP Architecture Diagram

```mermaid
flowchart TB
    CS[Cloud Scheduler\n(Cron Trigger)]
    CR[Cloud Run Job\n(Python ETL - Pandas)]
    SM[Secret Manager\n(API + BQ Credentials)]
    RAW[Cloud Storage\nRaw Landing Zone]
    BQ[BigQuery\nDim + Fact Tables]
    BQREP[BigQuery Scheduled Query\nAnalytical Report]
    BI[Looker Studio\nBI Dashboards]

    %% Data Flow
    CS --> CR
    SM --> CR
    CR --> RAW
    CR --> BQ
    BQ --> BQREP
    BQREP --> BI

    %% Strategy Notes (Not connected to graph)
    subgraph Scale [Scaling Strategy]
        A["Phase 1: Initial Lift & Shift\n• Pandas in Cloud Run\n(current implementation)"]
        B["Phase 2: Scale in Warehouse\n• Transformations in BigQuery SQL"]
        C["Phase 3: High Volume ETL\n• Dataflow / Dataproc for big/streaming jobs"]
    end
```
