from kafka import KafkaConsumer
import gtfs_realtime_pb2  # Import your protobuf definition

consumer = KafkaConsumer(
    "sncf-realtime",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="sncf-fixed-group",
)

print("✅ Consumer started and waiting for GTFS messages...")

for msg in consumer:
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(msg.value)  # Deserialize protobuf

        print("🟢 Received GTFS Realtime Feed:")
        for entity in feed.entity:
            print(f"  - Entity ID: {entity.id}")
            if entity.HasField("trip_update"):
                print(f"    🚆 Trip Update: {entity.trip_update}")
            if entity.HasField("vehicle"):
                print(f"    🚌 Vehicle Position: {entity.vehicle}")
            if entity.HasField("alert"):
                print(f"    ⚠️ Alert: {entity.alert}")

    except Exception as e:
        print(f"🔴 Error parsing GTFS message: {e}")
