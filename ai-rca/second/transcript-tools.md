## MCP tool: query

Arguments:

```json
{
  "expr": "sum by (service_name,span_name) (rate(traces_span_metrics_calls_total{span_kind=\"SPAN_KIND_SERVER\"}[2m]))",
  "time": "2026-10-25T15:32:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"service_name": "cart", "span_name": "POST /oteldemo.CartService/AddItem"}, "value": "0.15000500016667223"}, {"labels": {"service_name": "cart", "span_name": "POST /oteldemo.CartService/EmptyCart"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "cart", "span_name": "POST /oteldemo.CartService/GetCart"}, "value": "0.3166772225740858"}, {"labels": {"service_name": "ad", "span_name": "oteldemo.AdService/GetAds"}, "value": "0.06666888896296544"}, {"labels": {"service_name": "product-catalog", "span_name": "oteldemo.ProductCatalogService/GetProduct"}, "value": "0.6833561118703958"}, {"labels": {"service_name": "product-catalog", "span_name": "oteldemo.ProductCatalogService/ListProducts"}, "value": "0"}, {"labels": {"service_name": "payment", "span_name": "oteldemo.PaymentService/Charge"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "recommendation", "span_name": "oteldemo.RecommendationService/ListRecommendations"}, "value": "0.06666888896296544"}, {"labels": {"service_name": "image-provider", "span_name": "GET"}, "value": "0"}, {"labels": {"service_name": "image-provider", "span_name": "GET /status"}, "value": "0.30001000033334446"}, {"labels": {"service_name": "checkout", "span_name": "oteldemo.CheckoutService/PlaceOrder"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "currency", "span_name": "oteldemo.CurrencyService/Convert"}, "value": "0.11667055568518953"}, {"labels": {"service_name": "currency", "span_name": "oteldemo.CurrencyService/GetSupportedCurrencies"}, "value": "0"}, {"labels": {"service_name": "email", "span_name": "POST /send_order_confirmation"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "flagd", "span_name": "POST"}, "value": "0.13333777792593088"}, {"labels": {"service_name": "flagd", "span_name": "flagd.evaluation.v1.Service/EventStream"}, "value": "0"}, {"labels": {"service_name": "flagd", "span_name": "flagd.evaluation.v1.Service/ResolveAll"}, "value": "0"}, {"labels": {"service_name": "flagd", "span_name": "flagd.evaluation.v1.Service/ResolveInt"}, "value": "0.05000166672222408"}, {"labels": {"service_name": "flagd", "span_name": "flagd.evaluation.v2.Service/EventStream"}, "value": "0"}, {"labels": {"service_name": "flagd", "span_name": "flagd.evaluation.v2.Service/ResolveBoolean"}, "value": "0.8500283342778093"}, {"labels": {"service_name": "flagd", "span_name": "flagd.evaluation.v2.Service/ResolveFloat"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "flagd", "span_name": "resolveAll"}, "value": "0"}, {"labels": {"service_name": "flagd", "span_name": "resolveBoolean"}, "value": "0.8500283342778093"}, {"labels": {"service_name": "flagd", "span_name": "resolveFloat"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "flagd", "span_name": "resolveInt"}, "value": "0.05000166672222408"}, {"labels": {"service_name": "frontend", "span_name": "GET"}, "value": "0.26667555585186176"}, {"labels": {"service_name": "frontend", "span_name": "GET /"}, "value": "0.10000333344444816"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/cart"}, "value": "0.26667555585186176"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/currency"}, "value": "0"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/data"}, "value": "0.20000666688889632"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/products/[productId]/index"}, "value": "0.416680556018534"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/products/index"}, "value": "0"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/recommendations"}, "value": "0.10000333344444816"}, {"labels": {"service_name": "frontend", "span_name": "POST /api/cart"}, "value": "0.30001000033334446"}, {"labels": {"service_name": "frontend", "span_name": "POST /api/checkout"}, "value": "0.06666888896296544"}, {"labels": {"service_name": "frontend-proxy", "span_name": "GET"}, "value": "0.7666922230741026"}, {"labels": {"service_name": "frontend-proxy", "span_name": "POST"}, "value": "0.18333944464815496"}, {"labels": {"service_name": "quote", "span_name": "POST /getquote"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "shipping", "span_name": "POST /get-quote"}, "value": "0.03333444448148272"}, {"labels": {"service_name": "shipping", "span_name": "POST /ship-order"}, "value": "0.03333444448148272"}], "truncated_series": 1}
```

## MCP tool: alerts_at

Arguments:

```json
{
  "time": "2026-10-25T15:32:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"__name__": "ALERTS", "alertname": "CheckoutLatencyHigh", "alertstate": "firing", "service": "checkout", "severity": "P1", "system": "shop"}, "value": "1"}]}
```

## MCP tool: query_range

Arguments:

```json
{
  "expr": "sum by (service_name) (rate(traces_span_metrics_calls_total{span_kind=\"SPAN_KIND_SERVER\",status_code=\"STATUS_CODE_ERROR\"}[2m]))",
  "start": "2026-10-25T15:20:00Z",
  "end": "2026-10-25T15:42:00Z",
  "step": "60s"
}
```

Returned:

```json
{"resultType": "matrix", "result": [{"labels": {"service_name": "ad"}, "values": [[1792942080, "0.029914330477682587"], [1792942140, "0.01666750004166875"], [1792942200, "0.01666750004166875"], [1792942260, "0.05000166672222408"], [1792942320, "0.01666722224074136"], [1792942380, "0"], [1792942440, "0.01666722224074136"], [1792942500, "0.05000166672222408"], [1792942560, "0"], [1792942620, "0"], [1792942680, "0"], [1792942740, "0"], [1792942800, "0"], [1792942860, "0"], [1792942920, "0"]]}, {"labels": {"service_name": "flagd"}, "values": [[1792941600, "0"], [1792941660, "0"], [1792941720, "0"], [1792941780, "0"], [1792941840, "0"], [1792941900, "0"], [1792941960, "0"], [1792942020, "0"], [1792942080, "0.05000166672222408"], [1792942140, "0"], [1792942200, "0"], [1792942260, "0"], [1792942320, "0"], [1792942380, "0"], [1792942440, "0"], [1792942500, "0"], [1792942560, "0"], [1792942620, "0"], [1792942680, "0.01666750004166875"], [1792942740, "0"], [1792942800, "0"], [1792942860, "0"], [1792942920, "0"]]}, {"labels": {"service_name": "frontend"}, "values": [[1792942080, "0.059828660955365175"], [1792942140, "0.0333350000833375"], [1792942200, "0.0333350000833375"], [1792942260, "0.06666888896296544"], [1792942320, "0.06666888896296544"], [1792942380, "0"], [1792942440, "0.03333444448148272"], [1792942500, "0.10000333344444816"], [1792942560, "0"], [1792942620, "0"], [1792942680, "0"], [1792942740, "0"], [1792942800, "0"], [1792942860, "0"], [1792942920, "0"]]}, {"labels": {"service_name": "frontend-proxy"}, "values": [[1792942080, "0.2692289742991433"], [1792942140, "0.13334000033335"], [1792942200, "0.3000150007500375"], [1792942260, "0.18333944464815496"], [1792942320, "0.2500083336111204"], [1792942380, "0.15000750037501875"], [1792942440, "0.23334111137037905"], [1792942500, "0.06666888896296544"], [1792942560, "0"], [1792942620, "0"], [1792942680, "0"], [1792942740, "0"], [1792942800, "0"], [1792942860, "0"], [1792942920, "0"]]}]}
```

## MCP tool: query_range

Arguments:

```json
{
  "expr": "histogram_quantile(0.95,sum by (service_name,le) (rate(traces_span_metrics_duration_milliseconds_bucket{span_kind=\"SPAN_KIND_SERVER\",service_name=~\"checkout|payment|shipping|email|cart|currency|product-catalog|quote\"}[2m])))",
  "start": "2026-10-25T15:20:00Z",
  "end": "2026-10-25T15:42:00Z",
  "step": "60s"
}
```

Returned:

```json
{"resultType": "matrix", "result": [{"labels": {"service_name": "cart"}, "values": [[1792941600, "1.9327586206896554"], [1792941660, "1.9"], [1792941720, "1.9474999999999998"], [1792941780, "1.9395833333333332"], [1792941840, "1.9441860465116279"], [1792941900, "1.8999999999999997"], [1792941960, "1.9"], [1792942020, "1.9690909090909088"], [1792942080, "1.9633333333333334"], [1792942140, "1.9"], [1792942200, "3.2833333333333323"], [1792942260, "3.799999999999997"], [1792942320, "1.9"], [1792942380, "2"], [1792942440, "1.9826086956521738"], [1792942500, "1.9542857142857142"], [1792942560, "1.9"], [1792942620, "1.9"], [1792942680, "1.9237499999999996"], [1792942740, "1.9"], [1792942800, "1.9"], [1792942860, "1.935185185185185"], [1792942920, "1.9322033898305082"]]}, {"labels": {"service_name": "checkout"}, "values": [[1792941600, "48"], [1792941660, "48"], [1792941720, "48"], [1792941780, "48"], [1792941840, "48"], [1792941900, "48"], [1792941960, "48"], [1792942020, "48"], [1792942080, "48"], [1792942140, "48"], [1792942200, "48"], [1792942260, "13750"], [1792942320, "48"], [1792942380, "13749.999999999998"], [1792942440, "48"], [1792942500, "48"], [1792942560, "48"], [1792942620, "48"], [1792942680, "48"], [1792942740, "48"], [1792942800, "48"], [1792942860, "48"], [1792942920, "47.99999999999999"]]}, {"labels": {"service_name": "currency"}, "values": [[1792941600, "1.8999999999999997"], [1792941660, "1.9000000000000001"], [1792941720, "1.9"], [1792941780, "1.9"], [1792941840, "1.9000000000000001"], [1792941900, "1.9"], [1792941960, "1.9"], [1792942020, "1.9"], [1792942080, "1.9"], [1792942140, "1.9"], [1792942200, "1.9000000000000001"], [1792942260, "1.9"], [1792942320, "1.9"], [1792942380, "1.9000000000000001"], [1792942440, "1.9"], [1792942500, "1.9"], [1792942560, "1.9"], [1792942620, "1.8999999999999997"], [1792942680, "1.9"], [1792942740, "1.9"], [1792942800, "1.9"], [1792942860, "1.9"], [1792942920, "1.9000000000000001"]]}, {"labels": {"service_name": "email"}, "values": [[1792941600, "5.399999999999999"], [1792941660, "3.9000000000000004"], [1792941720, "3.9"], [1792941780, "3.9000000000000004"], [1792941840, "3.9"], [1792941900, "7.3"], [1792941960, "3.9"], [1792942020, "3.9"], [1792942080, "3.9"], [1792942140, "3.9000000000000004"], [1792942200, "5.6"], [1792942260, "5.5"], [1792942320, "3.9"], [1792942380, "5.499999999999999"], [1792942440, "3.9"], [1792942500, "5.6"], [1792942560, "3.8999999999999995"], [1792942620, "3.9"], [1792942680, "8.7"], [1792942740, "3.9"], [1792942800, "3.9"], [1792942860, "3.8666666666666667"], [1792942920, "3.8999999999999995"]]}, {"labels": {"service_name": "payment"}, "values": [[1792941600, "1.9"], [1792941660, "1.9"], [1792941720, "1.9"], [1792941780, "1.9"], [1792941840, "1.9"], [1792941900, "1.9"], [1792941960, "1.9"], [1792942020, "1.9"], [1792942080, "1.9"], [1792942140, "7.7"], [1792942200, "1.9"], [1792942260, "1.9000000000000001"], [1792942320, "1.9"], [1792942380, "1.9"], [1792942440, "1.9"], [1792942500, "1.9"], [1792942560, "1.8999999999999997"], [1792942620, "1.9"], [1792942680, "6.799999999999999"], [1792942740, "1.9"], [1792942800, "1.9"], [1792942860, "1.9"], [1792942920, "1.9"]]}, {"labels": {"service_name": "product-catalog"}, "values": [[1792941600, "4.774999999999999"], [1792941660, "6.2199999999999935"], [1792941720, "7.333333333333333"], [1792941780, "5.299999999999999"], [1792941840, "5.242857142857141"], [1792941900, "4.811111111111104"], [1792941960, "5.658333333333331"], [1792942020, "5.209999999999999"], [1792942080, "15000"], [1792942140, "15000"], [1792942200, "15000"], [1792942260, "15000"], [1792942320, "15000"], [1792942380, "15000"], [1792942440, "15000"], [1792942500, "15000"], [1792942560, "5.611111111111109"], [1792942620, "5.422222222222221"], [1792942680, "3.7899999999999943"], [1792942740, "5.377777777777778"], [1792942800, "5.145454545454543"], [1792942860, "5.871428571428571"], [1792942920, "5.545454545454544"]]}, {"labels": {"service_name": "quote"}, "values": [[1792941600, "1.9"], [1792941660, "1.9000000000000001"], [1792941720, "1.9"], [1792941780, "1.9000000000000001"], [1792941840, "1.9"], [1792941900, "1.9000000000000001"], [1792941960, "1.9"], [1792942020, "1.9"], [1792942080, "1.9"], [1792942140, "1.9000000000000001"], [1792942200, "1.9"], [1792942260, "1.9000000000000001"], [1792942320, "1.9"], [1792942380, "1.9"], [1792942440, "1.9"], [1792942500, "1.9"], [1792942560, "1.8999999999999997"], [1792942620, "1.9"], [1792942680, "1.9000000000000001"], [1792942740, "1.9"], [1792942800, "1.9"], [1792942860, "1.9"], [1792942920, "1.9"]]}, {"labels": {"service_name": "shipping"}, "values": [[1792941600, "1.9"], [1792941660, "1.9"], [1792941720, "1.9"], [1792941780, "1.9000000000000001"], [1792941840, "3.3999999999999995"], [1792941900, "1.9000000000000001"], [1792941960, "1.9"], [1792942020, "2.9999999999999982"], [1792942080, "1.9"], [1792942140, "1.9000000000000001"], [1792942200, "7.199999999999999"], [1792942260, "1.9000000000000001"], [1792942320, "3.5999999999999996"], [1792942380, "3.666666666666666"], [1792942440, "1.9"], [1792942500, "1.9"], [1792942560, "4.599999999999996"], [1792942620, "1.9"], [1792942680, "2"], [1792942740, "1.9"], [1792942800, "1.9"], [1792942860, "1.9"], [1792942920, "1.9"]]}]}
```

## MCP tool: list_metrics

Arguments:

```json
{
  "contains": ""
}
```

Returned:

```json
{"count": 721, "names": ["ALERTS", "ALERTS_FOR_STATE", "alertmanager_alerts", "alertmanager_alerts_invalid_total", "alertmanager_alerts_per_alert_limit", "alertmanager_alerts_received_total", "alertmanager_alerts_subscriber_channel_writes_total", "alertmanager_build_info", "alertmanager_cluster_enabled", "alertmanager_config_hash", "alertmanager_config_last_reload_success_timestamp_seconds", "alertmanager_config_last_reload_successful", "alertmanager_dispatcher_aggregation_group_creation_given_up_total", "alertmanager_dispatcher_aggregation_group_creation_retries_total", "alertmanager_dispatcher_aggregation_group_limit_reached_total", "alertmanager_dispatcher_aggregation_groups", "alertmanager_dispatcher_alert_processing_duration_seconds_count", "alertmanager_dispatcher_alert_processing_duration_seconds_sum", "alertmanager_http_concurrency_limit_exceeded_total", "alertmanager_http_request_duration_seconds_bucket", "alertmanager_http_request_duration_seconds_count", "alertmanager_http_request_duration_seconds_sum", "alertmanager_http_requests_in_flight", "alertmanager_http_response_size_bytes_bucket", "alertmanager_http_response_size_bytes_count", "alertmanager_http_response_size_bytes_sum", "alertmanager_inhibition_rules", "alertmanager_integrations", "alertmanager_nflog_gc_duration_seconds_count", "alertmanager_nflog_gc_duration_seconds_sum", "alertmanager_nflog_gossip_messages_propagated_total", "alertmanager_nflog_maintenance_errors_total", "alertmanager_nflog_maintenance_total", "alertmanager_nflog_queries_total", "alertmanager_nflog_query_duration_seconds_bucket", "alertmanager_nflog_query_duration_seconds_count", "alertmanager_nflog_query_duration_seconds_sum", "alertmanager_nflog_query_errors_total", "alertmanager_nflog_snapshot_duration_seconds_count", "alertmanager_nflog_snapshot_duration_seconds_sum", "alertmanager_nflog_snapshot_size_bytes", "alertmanager_notification_latency_seconds_bucket", "alertmanager_notification_latency_seconds_count", "alertmanager_notification_latency_seconds_sum", "alertmanager_notification_requests_failed_total", "alertmanager_notification_requests_total", "alertmanager_notifications_failed_total", "alertmanager_notifications_total", "alertmanager_receivers", "alertmanager_silences", "alertmanager_silences_gc_duration_seconds_count", "alertmanager_silences_gc_duration_seconds_sum", "alertmanager_silences_gc_errors_total", "alertmanager_silences_gossip_messages_propagated_total", "alertmanager_silences_maintenance_errors_total", "alertmanager_silences_maintenance_total", "alertmanager_silences_matcher_compile_errors_total", "alertmanager_silences_matcher_index_size", "alertmanager_silences_queries_total", "alertmanager_silences_query_duration_seconds_bucket", "alertmanager_silences_query_duration_seconds_count", "alertmanager_silences_query_duration_seconds_sum", "alertmanager_silences_query_errors_total", "alertmanager_silences_query_silences_scanned_total", "alertmanager_silences_query_silences_skipped_total", "alertmanager_silences_snapshot_duration_seconds_count", "alertmanager_silences_snapshot_duration_seconds_sum", "alertmanager_silences_snapshot_size_bytes", "alertmanager_silences_state_size", "alertmanager_silences_version_index_size", "aspnetcore_memory_pool_allocated_bytes_total", "aspnetcore_memory_pool_evicted_bytes_total", "aspnetcore_memory_pool_pooled_bytes", "aspnetcore_memory_pool_rented_bytes_total", "aspnetcore_routing_match_attempts_total", "container_blockio_io_service_bytes_recursive_total", "container_cpu_usage_kernelmode_nanoseconds_total", "container_cpu_usage_nanoseconds_total", "container_cpu_usage_system_nanoseconds_total", "container_cpu_usage_usermode_nanoseconds_total", "container_cpu_utilization_ratio", "container_memory_file_bytes", "container_memory_percent_ratio", "container_memory_usage_limit_bytes", "container_memory_usage_total_bytes", "container_network_io_usage_rx_bytes_total", "container_network_io_usage_rx_dropped_total", "container_network_io_usage_rx_packets_total", "container_network_io_usage_tx_bytes_total", "container_network_io_usage_tx_dropped_total", "container_network_io_usage_tx_packets_total", "container_uptime_seconds", "cpython_gc_collected_objects_total", "cpython_gc_collections_total", "cpython_gc_uncollectable_objects_total", "db_client_operation_duration_seconds_bucket", "db_client_operation_duration_seconds_count", "db_client_operation_duration_seconds_sum", "db_sql_connection_closed_max_idle_time_total", "db_sql_connection_closed_max_idle_total", "db_sql_connection_closed_max_lifetime_total", "db_sql_connection_max_open", "db_sql_connection_open", "db_sql_connection_wait_duration_milliseconds_total", "db_sql_connection_wait_total", "demo_ad_requests_total", "demo_cart_add_item_latency_seconds_bucket", "demo_cart_add_item_latency_seconds_count", "demo_cart_add_item_latency_seconds_sum", "demo_cart_get_cart_latency_seconds_bucket", "demo_cart_get_cart_latency_seconds_count", "demo_cart_get_cart_latency_seconds_sum", "demo_exchange_conversions_counter_total", "demo_notification_confirmations_total", "demo_payment_transactions_total", "demo_recommendation_requests_total", "demo_shipping_items_shipped_total", "dotnet_assembly_count", "dotnet_gc_collections_total", "dotnet_gc_heap_allocated_bytes_total", "dotnet_gc_last_collection_heap_fragmentation_size_bytes", "dotnet_gc_last_collection_heap_size_bytes", "dotnet_gc_last_collection_memory_committed_size_bytes", "dotnet_gc_pause_time_seconds_total", "dotnet_jit_compilation_time_seconds_total", "dotnet_jit_compiled_il_size_bytes_total", "dotnet_jit_compiled_methods_total", "dotnet_monitor_lock_contentions_total", "dotnet_process_cpu_count", "dotnet_process_cpu_time_seconds_total", "dotnet_process_memory_working_set_bytes", "dotnet_thread_pool_queue_length_total", "dotnet_thread_pool_thread_count_total", "dotnet_thread_pool_work_item_count_total", "dotnet_timer_count", "feature_flag_evaluation_active_count", "feature_flag_evaluation_requests_total", "feature_flag_evaluation_success_total", "go_config_gogc_percent", "go_gc_cleanups_executed_cleanups_total", "go_gc_cleanups_queued_cleanups_total", "go_gc_cycles_automatic_gc_cycles_total", "go_gc_cycles_forced_gc_cycles_total", "go_gc_cycles_total_gc_cycles_total", "go_gc_duration_seconds", "go_gc_duration_seconds_count", "go_gc_duration_seconds_sum", "go_gc_finalizers_executed_finalizers_total", "go_gc_finalizers_queued_finalizers_total", "go_gc_gogc_percent", "go_gc_gomemlimit_bytes", "go_gc_heap_allocs_by_size_bytes_bucket", "go_gc_heap_allocs_by_size_bytes_count", "go_gc_heap_allocs_by_size_bytes_sum", "go_gc_heap_allocs_bytes_total", "go_gc_heap_allocs_objects_total", "go_gc_heap_frees_by_size_bytes_bucket", "go_gc_heap_frees_by_size_bytes_count", "go_gc_heap_frees_by_size_bytes_sum", "go_gc_heap_frees_bytes_total", "go_gc_heap_frees_objects_total", "go_gc_heap_goal_bytes", "go_gc_heap_live_bytes", "go_gc_heap_objects_objects", "go_gc_heap_tiny_allocs_objects_total", "go_gc_limiter_last_enabled_gc_cycle", "go_gc_pauses_seconds_bucket", "go_gc_pauses_seconds_count", "go_gc_pauses_seconds_sum", "go_gc_scan_globals_bytes", "go_gc_scan_heap_bytes", "go_gc_scan_stack_bytes", "go_gc_scan_total_bytes", "go_gc_stack_starting_size_bytes", "go_goroutine_count", "go_goroutines", "go_info", "go_memory_allocated_bytes_total", "go_memory_allocations_total", "go_memory_gc_goal_bytes", "go_memory_limit_bytes", "go_memory_used_bytes", "go_memstats_alloc_bytes", "go_memstats_alloc_bytes_total", "go_memstats_buck_hash_sys_bytes", "go_memstats_frees_total", "go_memstats_gc_sys_bytes", "go_memstats_heap_alloc_bytes", "go_memstats_heap_idle_bytes", "go_memstats_heap_inuse_bytes", "go_memstats_heap_objects", "go_memstats_heap_released_bytes", "go_memstats_heap_sys_bytes", "go_memstats_last_gc_time_seconds", "go_memstats_mallocs_total", "go_memstats_mcache_inuse_bytes", "go_memstats_mcache_sys_bytes", "go_memstats_mspan_inuse_bytes", "go_memstats_mspan_sys_bytes", "go_memstats_next_gc_bytes"]}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "sum by (service_name,span_name,status_code) (rate(traces_span_metrics_calls_total{span_kind=\"SPAN_KIND_SERVER\",service_name=~\"checkout|product-catalog|ad|frontend\"}[2m]))",
  "time": "2026-10-25T15:31:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"service_name": "ad", "span_name": "oteldemo.AdService/GetAds", "status_code": "STATUS_CODE_ERROR"}, "value": "0.05000166672222408"}, {"labels": {"service_name": "ad", "span_name": "oteldemo.AdService/GetAds", "status_code": "STATUS_CODE_UNSET"}, "value": "0.13333777792593088"}, {"labels": {"service_name": "product-catalog", "span_name": "oteldemo.ProductCatalogService/GetProduct", "status_code": "STATUS_CODE_UNSET"}, "value": "1.483382779425981"}, {"labels": {"service_name": "product-catalog", "span_name": "oteldemo.ProductCatalogService/ListProducts", "status_code": "STATUS_CODE_UNSET"}, "value": "0.13333777792593088"}, {"labels": {"service_name": "checkout", "span_name": "oteldemo.CheckoutService/PlaceOrder", "status_code": "STATUS_CODE_UNSET"}, "value": "0.08333611120370679"}, {"labels": {"service_name": "frontend", "span_name": "GET", "status_code": "STATUS_CODE_UNSET"}, "value": "0.30001000033334446"}, {"labels": {"service_name": "frontend", "span_name": "GET /", "status_code": "STATUS_CODE_UNSET"}, "value": "0.10000333344444816"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/cart", "status_code": "STATUS_CODE_UNSET"}, "value": "0.26667555585186176"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/currency", "status_code": "STATUS_CODE_UNSET"}, "value": "0"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/data", "status_code": "STATUS_CODE_ERROR"}, "value": "0.06666888896296544"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/data", "status_code": "STATUS_CODE_UNSET"}, "value": "0.23334111137037905"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/products/[productId]/index", "status_code": "STATUS_CODE_UNSET"}, "value": "0.883362778759292"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/products/index", "status_code": "STATUS_CODE_UNSET"}, "value": "0.08333611120370679"}, {"labels": {"service_name": "frontend", "span_name": "GET /api/recommendations", "status_code": "STATUS_CODE_UNSET"}, "value": "0.23334111137037905"}, {"labels": {"service_name": "frontend", "span_name": "POST /api/cart", "status_code": "STATUS_CODE_UNSET"}, "value": "0.40001333377779263"}, {"labels": {"service_name": "frontend", "span_name": "POST /api/checkout", "status_code": "STATUS_CODE_UNSET"}, "value": "0.16667222240741358"}]}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "histogram_quantile(0.95,sum by (service_name,span_name,span_kind,le) (rate(traces_span_metrics_duration_milliseconds_bucket{service_name=~\"checkout|product-catalog|ad\"}[2m])))",
  "time": "2026-10-25T15:31:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.CartService/GetCart"}, "value": "1.9000000000000001"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.PaymentService/Charge"}, "value": "3.5"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_INTERNAL", "span_name": "prepareOrderItemsAndShippingQuoteFromCart"}, "value": "13750"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.CheckoutService/PlaceOrder"}, "value": "13750"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_CLIENT", "span_name": "flagd.evaluation.v2.Service/ResolveBoolean"}, "value": "NaN"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.AdService/GetAds"}, "value": "3.4499999999999997"}, {"labels": {"service_name": "product-catalog", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.ProductCatalogService/GetProduct"}, "value": "15000"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_CLIENT", "span_name": "resolve"}, "value": "NaN"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_INTERNAL", "span_name": "getRandomAds"}, "value": "1.9"}, {"labels": {"service_name": "product-catalog", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.ProductCatalogService/ListProducts"}, "value": "15000"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_CLIENT", "span_name": "flagd.evaluation.v2.Service/EventStream"}, "value": "NaN"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_INTERNAL", "span_name": "getAdsByCategory"}, "value": "1.9"}, {"labels": {"service_name": "product-catalog", "span_kind": "SPAN_KIND_CLIENT", "span_name": "astronomy-db"}, "value": "15000"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "POST"}, "value": "5.249999999999999"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.CartService/EmptyCart"}, "value": "3.5"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.CurrencyService/Convert"}, "value": "2.6000000000000005"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.ProductCatalogService/GetProduct"}, "value": "12749.999999999996"}]}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "container_cpu_utilization_ratio",
  "time": "2026-10-25T15:31:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "alertmanager", "host_name": "itsm-playground"}, "value": "0.01760898507530428"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "astronomy-db", "host_name": "itsm-playground"}, "value": "0.6351973268054133"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "cart", "host_name": "itsm-playground"}, "value": "0.3500812423882539"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "checkout", "host_name": "itsm-playground"}, "value": "0.2940782302504926"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "currency", "host_name": "itsm-playground"}, "value": "0.2589684093079549"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "email", "host_name": "itsm-playground"}, "value": "0.8658508333735198"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "flagd", "host_name": "itsm-playground"}, "value": "0.1255062232463759"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "flagd-ui", "host_name": "itsm-playground"}, "value": "0.3965169866306343"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "frontend", "host_name": "itsm-playground"}, "value": "0.9360305298760292"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "frontend-proxy", "host_name": "itsm-playground"}, "value": "0.4746174422903632"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "grafana", "host_name": "itsm-playground"}, "value": "0.8349337687916693"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "image-provider", "host_name": "itsm-playground"}, "value": "0.24935154235507592"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "jaeger", "host_name": "itsm-playground"}, "value": "0.17270146482048102"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "kb-index", "host_name": "itsm-playground"}, "value": "0.0009223516241002042"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "load-generator", "host_name": "itsm-playground"}, "value": "0.9865193127771631"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "opamp-server", "host_name": "itsm-playground"}, "value": "0.22149475358342027"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "opensearch", "host_name": "itsm-playground"}, "value": "2.524510797877018"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "otel-collector", "host_name": "itsm-playground"}, "value": "1.7730736332699497"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "pager", "host_name": "itsm-playground"}, "value": "0.23673928418791296"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "payment", "host_name": "itsm-playground"}, "value": "5.060969979263764"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "product-catalog", "host_name": "itsm-playground"}, "value": "0.4061299046120562"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "prometheus", "host_name": "itsm-playground"}, "value": "0.26293357136305745"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "quote", "host_name": "itsm-playground"}, "value": "0.3564886707370002"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "recommendation", "host_name": "itsm-playground"}, "value": "0.7121120650529501"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "seeded-flagd", "host_name": "itsm-playground"}, "value": "0.24577537740612362"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "shipping", "host_name": "itsm-playground"}, "value": "0.2415074394293538"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "svcdesk", "host_name": "itsm-playground"}, "value": "0.10831395568734539"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "telemetry-docs", "host_name": "itsm-playground"}, "value": "0.26446540838875054"}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "valkey-cart", "host_name": "itsm-playground"}, "value": "0.31279435403043104"}]}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "histogram_quantile(0.95,sum by (service_name,span_name,span_kind,le) (rate(traces_span_metrics_duration_milliseconds_bucket{service_name=~\"checkout|product-catalog|ad\"}[2m])))",
  "time": "2026-10-25T15:25:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_INTERNAL", "span_name": "getAdsByCategory"}, "value": "1.9"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.CartService/EmptyCart"}, "value": "1.9"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.ProductCatalogService/GetProduct"}, "value": "1.9"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_CLIENT", "span_name": "flagd.evaluation.v2.Service/EventStream"}, "value": "NaN"}, {"labels": {"service_name": "product-catalog", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.ProductCatalogService/ListProducts"}, "value": "1.9"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "POST"}, "value": "5.899999999999997"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.CurrencyService/Convert"}, "value": "1.9"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_INTERNAL", "span_name": "prepareOrderItemsAndShippingQuoteFromCart"}, "value": "9.65"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_CLIENT", "span_name": "flagd.evaluation.v2.Service/ResolveBoolean"}, "value": "NaN"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.AdService/GetAds"}, "value": "5.499999999999999"}, {"labels": {"service_name": "product-catalog", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.ProductCatalogService/GetProduct"}, "value": "4.8999999999999995"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.CartService/GetCart"}, "value": "1.9"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_CLIENT", "span_name": "resolve"}, "value": "NaN"}, {"labels": {"service_name": "ad", "span_kind": "SPAN_KIND_INTERNAL", "span_name": "getRandomAds"}, "value": "1.9"}, {"labels": {"service_name": "product-catalog", "span_kind": "SPAN_KIND_CLIENT", "span_name": "astronomy-db"}, "value": "1.8999999999999997"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_CLIENT", "span_name": "oteldemo.PaymentService/Charge"}, "value": "3.3"}, {"labels": {"service_name": "checkout", "span_kind": "SPAN_KIND_SERVER", "span_name": "oteldemo.CheckoutService/PlaceOrder"}, "value": "48"}]}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "{__name__=~\"db_sql_connection_open|db_sql_connection_max_open|db_sql_connection_wait_total|db_sql_connection_wait_duration_milliseconds_total\"}",
  "time": "2026-10-25T15:31:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"__name__": "db_sql_connection_max_open", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0"}, "value": "0"}, {"labels": {"__name__": "db_sql_connection_open", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0", "status": "idle"}, "value": "0"}, {"labels": {"__name__": "db_sql_connection_open", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0", "status": "inuse"}, "value": "12"}, {"labels": {"__name__": "db_sql_connection_wait_duration_milliseconds_total", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0"}, "value": "0"}, {"labels": {"__name__": "db_sql_connection_wait_total", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0"}, "value": "0"}]}
```

## MCP tool: query_range

Arguments:

```json
{
  "expr": "container_cpu_utilization_ratio{container_name=~\"payment|astronomy-db|checkout\"}",
  "start": "2026-10-25T15:20:00Z",
  "end": "2026-10-25T15:42:00Z",
  "step": "60s"
}
```

Returned:

```json
{"resultType": "matrix", "result": [{"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "astronomy-db", "host_name": "itsm-playground"}, "values": [[1792941600, "0.48055107611893855"], [1792941660, "0.5008097970966111"], [1792941720, "0.5154658396937467"], [1792941780, "0.5306867923129668"], [1792941840, "0.5434379981681494"], [1792941900, "0.5553497685169956"], [1792941960, "0.568312523364486"], [1792942020, "0.5814394043499445"], [1792942080, "0.5930119099478376"], [1792942140, "0.6080703774652577"], [1792942200, "0.6203426197969287"], [1792942260, "0.6351973268054133"], [1792942320, "0.6461384048244981"], [1792942380, "0.6583534709193246"], [1792942440, "0.666285202638019"], [1792942500, "0.6746014565562354"], [1792942560, "0.6817600194106065"], [1792942620, "0.6885480358419364"], [1792942680, "0.6937770799707008"], [1792942740, "0.6994613301931033"], [1792942800, "0.7063942714239699"], [1792942860, "0.7132868793521768"], [1792942920, "0.719913152647961"]]}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "checkout", "host_name": "itsm-playground"}, "values": [[1792941600, "0.2225664198193047"], [1792941660, "0.2311188182969574"], [1792941720, "0.23850179730928023"], [1792941780, "0.24686203150084207"], [1792941840, "0.25410850180535915"], [1792941900, "0.2607092407007971"], [1792941960, "0.2673445318733291"], [1792942020, "0.27346196609491924"], [1792942080, "0.2789742256630428"], [1792942140, "0.2845360624496442"], [1792942200, "0.28923524470543605"], [1792942260, "0.2940782302504926"], [1792942320, "0.2983379875745164"], [1792942380, "0.3026455560347673"], [1792942440, "0.3065301384334704"], [1792942500, "0.31141589294639094"], [1792942560, "0.31557626642709474"], [1792942620, "0.32005379736050465"], [1792942680, "0.32384849721800585"], [1792942740, "0.3274160534956739"], [1792942800, "0.3308788948161593"], [1792942860, "0.3345658015149767"], [1792942920, "0.3379725435871498"]]}, {"labels": {"__name__": "container_cpu_utilization_ratio", "container_name": "payment", "host_name": "itsm-playground"}, "values": [[1792941600, "3.7950387855787477"], [1792941660, "3.9468627795117386"], [1792941720, "4.083382123510939"], [1792941780, "4.218004114082393"], [1792941840, "4.346769310847153"], [1792941900, "4.461912396993273"], [1792941960, "4.57017188913562"], [1792942020, "4.67348859676793"], [1792942080, "4.768671087236872"], [1792942140, "4.88671038353175"], [1792942200, "4.975933215134599"], [1792942260, "5.060969979263764"], [1792942320, "5.142085975088392"], [1792942380, "5.222884805610258"], [1792942440, "5.296373761522114"], [1792942500, "5.370802269752713"], [1792942560, "5.442442671155129"], [1792942620, "5.509527312504728"], [1792942680, "5.571343411027669"], [1792942740, "5.643236066938454"], [1792942800, "5.7098565389733436"], [1792942860, "5.765948606737339"], [1792942920, "5.820920512957948"]]}]}
```

## MCP tool: query_range

Arguments:

```json
{
  "expr": "db_sql_connection_open{service_name=\"product-catalog\"}",
  "start": "2026-10-25T15:20:00Z",
  "end": "2026-10-25T15:42:00Z",
  "step": "60s"
}
```

Returned:

```json
{"resultType": "matrix", "result": [{"labels": {"__name__": "db_sql_connection_open", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0", "status": "idle"}, "values": [[1792941600, "2"], [1792941660, "2"], [1792941720, "2"], [1792941780, "2"], [1792941840, "2"], [1792941900, "2"], [1792941960, "2"], [1792942020, "0"], [1792942080, "0"], [1792942140, "0"], [1792942200, "0"], [1792942260, "0"], [1792942320, "0"], [1792942380, "0"], [1792942440, "0"], [1792942500, "2"], [1792942560, "2"], [1792942620, "2"], [1792942680, "2"], [1792942740, "2"], [1792942800, "2"], [1792942860, "2"], [1792942920, "2"]]}, {"labels": {"__name__": "db_sql_connection_open", "db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0", "status": "inuse"}, "values": [[1792941600, "0"], [1792941660, "0"], [1792941720, "0"], [1792941780, "0"], [1792941840, "0"], [1792941900, "0"], [1792941960, "0"], [1792942020, "8"], [1792942080, "14"], [1792942140, "11"], [1792942200, "27"], [1792942260, "12"], [1792942320, "18"], [1792942380, "10"], [1792942440, "17"], [1792942500, "0"], [1792942560, "0"], [1792942620, "0"], [1792942680, "0"], [1792942740, "0"], [1792942800, "0"], [1792942860, "0"], [1792942920, "0"]]}]}
```

## MCP tool: query_range

Arguments:

```json
{
  "expr": "histogram_quantile(0.95,sum by (service_name,le) (rate(db_client_operation_duration_seconds_bucket{service_name=\"product-catalog\"}[2m])))",
  "start": "2026-10-25T15:20:00Z",
  "end": "2026-10-25T15:42:00Z",
  "step": "60s"
}
```

Returned:

```json
{"resultType": "matrix", "result": [{"labels": {"service_name": "product-catalog"}, "values": [[1792941600, "0.0009616564417177913"], [1792941660, "0.0009752212389380531"], [1792941720, "0.000980115273775216"], [1792941780, "0.0009672335600907028"], [1792941840, "0.0009563973063973063"], [1792941900, "0.0009664739884393063"], [1792941960, "0.0009697916666666668"], [1792942020, "0.00097583081570997"], [1792942080, "10"], [1792942140, "10"], [1792942200, "10"], [1792942260, "10"], [1792942320, "10"], [1792942380, "10"], [1792942440, "10"], [1792942500, "2.3999999999999786"], [1792942560, "0.0009623376623376623"], [1792942620, "0.0009652243589743589"], [1792942680, "0.000963701923076923"], [1792942740, "0.0009744485294117648"], [1792942800, "0.000974234693877551"], [1792942860, "0.0009618012422360248"], [1792942920, "0.0009589834515366429"]]}]}
```

## MCP tool: list_metrics

Arguments:

```json
{
  "contains": "pg_"
}
```

Returned:

```json
{"count": 0, "names": []}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "sum by (service_name,span_name) (rate(traces_span_metrics_calls_total{span_kind=\"SPAN_KIND_SERVER\",service_name=~\"checkout|product-catalog|payment|ad|frontend\",status_code=\"STATUS_CODE_ERROR\"}[2m]))",
  "time": "2026-10-25T15:25:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": []}
```

## MCP tool: query

Arguments:

```json
{
  "expr": "sum by (le) (rate(traces_span_metrics_duration_milliseconds_bucket{service_name=\"product-catalog\",span_kind=\"SPAN_KIND_CLIENT\",span_name=\"astronomy-db\"}[2m]))",
  "time": "2026-10-25T15:31:00Z"
}
```

Returned:

```json
{"resultType": "vector", "result": [{"labels": {"le": "+Inf"}, "value": "1.71672389079636"}, {"labels": {"le": "10"}, "value": "1.0000333344444816"}, {"labels": {"le": "100"}, "value": "1.0000333344444816"}, {"labels": {"le": "1000"}, "value": "1.0000333344444816"}, {"labels": {"le": "10000"}, "value": "1.2333744458148606"}, {"labels": {"le": "1400"}, "value": "1.0000333344444816"}, {"labels": {"le": "15000"}, "value": "1.2667088902963433"}, {"labels": {"le": "2"}, "value": "0.9666988899629989"}, {"labels": {"le": "200"}, "value": "1.0000333344444816"}, {"labels": {"le": "2000"}, "value": "1.016700556685223"}, {"labels": {"le": "4"}, "value": "0.9833661122037403"}, {"labels": {"le": "400"}, "value": "1.0000333344444816"}, {"labels": {"le": "50"}, "value": "1.0000333344444816"}, {"labels": {"le": "5000"}, "value": "1.1000366678889297"}, {"labels": {"le": "6"}, "value": "1.0000333344444816"}, {"labels": {"le": "8"}, "value": "1.0000333344444816"}, {"labels": {"le": "800"}, "value": "1.0000333344444816"}]}
```

## MCP tool: query_range

Arguments:

```json
{
  "expr": "rate(db_sql_connection_wait_total{service_name=\"product-catalog\"}[2m])",
  "start": "2026-10-25T15:20:00Z",
  "end": "2026-10-25T15:42:00Z",
  "step": "60s"
}
```

Returned:

```json
{"resultType": "matrix", "result": [{"labels": {"db_system_name": "postgresql", "host_name": "itsm-playground", "instance": "396a193951021f05b8b0c9e89092b1b6", "job": "opentelemetry-demo/product-catalog", "server_address": "astronomy-db", "service_criticality": "high", "service_instance_id": "396a193951021f05b8b0c9e89092b1b6", "service_name": "product-catalog", "service_namespace": "opentelemetry-demo", "service_version": "3.1.0"}, "values": [[1792941600, "0"], [1792941660, "0"], [1792941720, "0"], [1792941780, "0"], [1792941840, "0"], [1792941900, "0"], [1792941960, "0"], [1792942020, "0"], [1792942080, "0"], [1792942140, "0"], [1792942200, "0"], [1792942260, "0"], [1792942320, "0"], [1792942380, "0"], [1792942440, "0"], [1792942500, "0"], [1792942560, "0"], [1792942620, "0"], [1792942680, "0"], [1792942740, "0"], [1792942800, "0"], [1792942860, "0"], [1792942920, "0"]]}]}
```

