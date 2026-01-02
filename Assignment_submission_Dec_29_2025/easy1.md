Kafka streaming is a way to process data continuously as events happen instead of waiting for batch files.

Producers publish events (messages) to Kafka.

Kafka stores events in topics (like categories).

Each topic is split into partitions (for scaling).

Consumers read events from topics.

A consumer group lets multiple consumers share the work (each partition goes to only one consumer in the group).

Streaming apps process events in real time:

filtering (only keep some events),

transformations (edit/clean fields),

aggregations (count, sum, average),

windowing (compute metrics per last 10 seconds / last 5 minutes),

and write results to another topic/database.