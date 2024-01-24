from dagster import (
    AssetExecutionContext,
    AutoMaterializePolicy,
    AutoMaterializeRule,
    BackfillPolicy,
    DailyPartitionsDefinition,
    MultiPartitionsDefinition,
    RetryPolicy,
    SourceAsset,
    StaticPartitionsDefinition,
    asset,
)


@asset(
    deps=[SourceAsset(key="ga_hits"), SourceAsset(key="drupal_st")],
    compute_kind="pyspark",
    code_version="v1.0.3",
    partitions_def=MultiPartitionsDefinition(
        {
            "date": DailyPartitionsDefinition(start_date="2024-01-17", timezone="Asia/Singapore"),
            "publication": StaticPartitionsDefinition(["st"]),
        }
    ),
    backfill_policy=BackfillPolicy.multi_run(max_partitions_per_run=2),
    auto_materialize_policy=AutoMaterializePolicy.eager(max_materializations_per_minute=2).with_rules(
        AutoMaterializeRule.skip_on_not_all_parents_updated()
    ),
)
def lumos_ga_hits(context: AssetExecutionContext) -> None:
    print("getting lumos_ga_hits")
    context.log.info("getting lumos_ga_hits")
    print("lumos_ga_hits retrieved")
    context.log.info("lumos_ga_hits retrieved")


@asset(
    deps=[lumos_ga_hits],
    compute_kind="pyspark",
    retry_policy=RetryPolicy(max_retries=1, delay=5),
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def lumos_article(context: AssetExecutionContext) -> None:
    print("getting lumos article")
    context.log.info("getting lumos article")
    raise ValueError("asd")
    print("lumos article retrieved")
    context.log.info("lumos article retrieved")
