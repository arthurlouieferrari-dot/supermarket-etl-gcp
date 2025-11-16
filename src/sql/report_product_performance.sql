WITH sales_enriched AS (
    SELECT
        f.sale_id,
        f.invoice_id,
        f.date,
        f.time,
        f.unit_price,
        f.quantity,
        f.tax_amount,
        f.total_amount,
        f.cogs,
        f.gross_margin_pct,
        f.gross_income,
        f.rating,

        dloc.branch,
        dloc.city,
        dprod.product_line,
        dseg.customer_type,
        dseg.gender
    FROM fact_sales f
    JOIN dim_location dloc
        ON f.location_id = dloc.location_id
    JOIN dim_product dprod
        ON f.product_id = dprod.product_id
    JOIN dim_customer_segment dseg
        ON f.customer_segment_id = dseg.customer_segment_id
),

agg AS (
    SELECT
        branch,
        city,
        product_line,

        COUNT(*) AS num_transactions,
        SUM(quantity) AS total_units_sold,
        SUM(total_amount) AS total_revenue,
        SUM(gross_income) AS total_gross_income,

        AVG(unit_price) AS avg_unit_price,
        AVG(rating) AS avg_rating,
        AVG(total_amount) AS avg_transaction_amount,

        -- Measures needed for window functions
        SUM(total_amount) OVER (PARTITION BY branch, city) AS location_total_revenue,
        COUNT(*) OVER (PARTITION BY branch, city) AS location_total_transactions
    FROM sales_enriched
    GROUP BY
        branch, city, product_line
)

SELECT
    *,

    -- % of revenue for this product in this location
    ROUND(total_revenue * 1.0 / location_total_revenue, 4)
        AS pct_of_location_revenue,

    -- Percent rank of the product based on revenue
    PERCENT_RANK() OVER (
        PARTITION BY branch, city
        ORDER BY total_revenue
    ) AS revenue_percent_rank,

    -- Dense rank (no ties skipped)
    DENSE_RANK() OVER (
        PARTITION BY branch, city
        ORDER BY total_revenue DESC
    ) AS revenue_dense_rank,

    -- Running revenue by product across locations
    SUM(total_revenue) OVER (
        PARTITION BY branch, city
        ORDER BY total_revenue DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue,

    -- Cumulative % of revenue (Pareto / 80-20 curve)
    ROUND(
        SUM(total_revenue) OVER (
            PARTITION BY branch, city
            ORDER BY total_revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) / location_total_revenue,
        4
    ) AS cumulative_revenue_pct

FROM agg
ORDER BY branch, city, total_revenue DESC;
