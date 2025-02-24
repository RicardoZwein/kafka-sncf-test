from kafka import KafkaProducer
import requests
import time
import gtfs_realtime_pb2  # Import the GTFS Protobuf schema

KAFKA_BROKER = "localhost:9092"
TOPIC = "sncf-realtime"

# Create Kafka Producer with longer timeouts
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    retries=5,  # Retry sending messages
    request_timeout_ms=30000,  # Increase timeout (default is 10000ms)
    linger_ms=500,  # Small delay to batch messages
    max_block_ms=60000,  # Maximum time to block when sending
    buffer_memory=67108864,  # 64MB buffer (default is 32MB)
)

def fetch_data():
    url = "https://proxy.transport.data.gouv.fr/resource/sncf-ter-gtfs-rt-trip-updates"
    response = requests.get(url)

    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        serialized_data = feed.SerializeToString()
        print(f"✅ Fetched {len(feed.entity)} entities")
        print(f"🔄 Serialized {len(serialized_data)} bytes")

        if len(serialized_data) > 10485760:  # 10MB limit (Kafka default)
            print("⚠️ Data too large, consider compression or splitting!")
        return serialized_data

    print("⚠️ No valid data fetched")
    return None

while True:
    data = fetch_data()
    if data:
        try:
            future = producer.send(TOPIC, value=data)
            future.get(timeout=20)  # Blocks until Kafka confirms
            print("✅ Successfully sent message to Kafka")
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
    time.sleep(120)  # Fetch every 2 minutes
