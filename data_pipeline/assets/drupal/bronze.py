import warnings

import pandas as pd
from dagster import (
    AssetExecutionContext,
    AutoMaterializePolicy,
    AutoMaterializeRule,
    ExperimentalWarning,
    FreshnessPolicy,
    MaterializeResult,
    MetadataValue,
    asset,
)

warnings.filterwarnings("ignore", category=ExperimentalWarning)


@asset(
    compute_kind="JDBC",
    auto_materialize_policy=AutoMaterializePolicy.eager().with_rules(
        AutoMaterializeRule.materialize_on_cron(cron_schedule="53 20 * * *", timezone="Asia/Singapore")
    ),
)
def drupal_bt(context: AssetExecutionContext) -> None:
    print("getting drupal data")
    context.log.info("getting drupal")
    print("drupal data retrieved")
    context.log.info("drupal retrieved")


@asset(
    deps=[drupal_bt],
    metadata={"owner": "Abdul"},
    compute_kind="pyspark",
    freshness_policy=(
        FreshnessPolicy(
            maximum_lag_minutes=1,
            cron_schedule="07 12 * * *",
            cron_schedule_timezone="Asia/Singapore",
        )
    ),
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def drupal_bt_silver(context: AssetExecutionContext) -> None:
    print("getting drupal_silver")
    context.log.info("getting drupal_silver")
    df = pd.DataFrame([[1, 2]], columns=["col_a", "col_b"])
    print("drupal_silver retrieved")
    context.log.info("drupal_silver retrieved")
    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )
