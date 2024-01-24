from dagster import (
    AssetExecutionContext,
    AutoMaterializePolicy,
    AutoMaterializeRule,
    BackfillPolicy,
    DailyPartitionsDefinition,
    MultiPartitionKey,
    MultiPartitionsDefinition,
    StaticPartitionsDefinition,
    asset,
)

StaticPartitionsDefinition(["red", "yellow", "blue"])


@asset(
    compute_kind="JDBC",
    partitions_def=MultiPartitionsDefinition(
        {
            "date": DailyPartitionsDefinition(start_date="2024-01-17", timezone="Asia/Singapore"),
            "publication": StaticPartitionsDefinition(["st", "bt", "zb"]),
        }
    ),
    backfill_policy=BackfillPolicy.multi_run(max_partitions_per_run=2),
    # auto_materialize_policy=AutoMaterializePolicy.eager(
    #     max_materializations_per_minute=10
    # ).with_rules(
    #     AutoMaterializeRule.materialize_on_cron(
    #         cron_schedule="41 22 * * *", timezone="Asia/Singapore"
    #     )
    # ),
)
def ga(context: AssetExecutionContext) -> None:
    context.log.info(f"{context.partition_keys}")
    if isinstance(context.partition_keys[0], MultiPartitionKey):
        context.log.info(context.partition_keys[0].keys_by_dimension)
    context.log.info("getting ga data")
    print("ga data retrieved")
    context.log.info("ga data retrieved")


@asset(
    deps=[ga],
    partitions_def=MultiPartitionsDefinition(
        {
            "date": DailyPartitionsDefinition(start_date="2024-01-17", timezone="Asia/Singapore"),
            "publication": StaticPartitionsDefinition(["st", "bt", "zb"]),
        }
    ),
    compute_kind="pyspark",
    backfill_policy=BackfillPolicy.multi_run(max_partitions_per_run=2),
    auto_materialize_policy=AutoMaterializePolicy.eager(max_materializations_per_minute=10),
)
def ga_hits(context: AssetExecutionContext) -> None:
    print("getting ga hits")
    context.log.info(f"{context.partition_keys}")
    context.log.info("getting ga hits")
    print("ga hits retrieved")
    context.log.info("ga hits retrieved")
