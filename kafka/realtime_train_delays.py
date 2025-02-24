import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import threading
from kafka import KafkaConsumer
import gtfs_realtime_pb2
import time

# ✅ Global list to store delays
delays = []

# ✅ Kafka Consumer Function (Runs in Background)
def consume_kafka():
    print("✅ Kafka Consumer Started...")
    consumer = KafkaConsumer(
        "sncf-realtime",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        enable_auto_commit=False,
        group_id="sncf-live-group",
    )
    for msg in consumer:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(msg.value)
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                for stop in entity.trip_update.stop_time_update:
                    delay = stop.arrival.delay if stop.HasField("arrival") else 0
                    delay_minutes = delay / 60  # Convert to minutes
                    
                    if delay_minutes >= 0:
                        delays.append(delay_minutes)

        # ✅ Debugging
        print(f"📡 Received {len(delays)} total delays.")

# ✅ Start Kafka Consumer in a Separate Thread
threading.Thread(target=consume_kafka, daemon=True).start()

# ✅ Custom Bins for Delays
bins = [0, 1, 5, 10, 20, 50, float('inf')]  # 50+ goes to infinity
labels = ["0", "1-5", "6-10", "11-20", "21-50", "50+"]

# ✅ Dash App Setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time Train Delay Distribution"),
    dcc.Graph(id="live-histogram"),
    dcc.Interval(id="interval", interval=2000, n_intervals=0)  # Update every 2 sec
])

@app.callback(
    Output("live-histogram", "figure"),
    [Input("interval", "n_intervals")]
)
def update_histogram(n):
    if not delays:
        print("⚠️ No new data received yet.")
        return go.Figure(layout={"title": "Waiting for Data..."})  # Empty but clear

    df = pd.DataFrame({"delays": delays})

    # ✅ **Bin the delays manually**
    df["binned"] = pd.cut(df["delays"], bins=bins, labels=labels, right=False)

    # ✅ **Count occurrences per bin**
    delay_counts = df["binned"].value_counts().reindex(labels, fill_value=0)

    # ✅ **Debugging**
    print(f"📊 Updated Histogram | Data: {delay_counts.to_dict()}")

    # ✅ **Create Plotly Bar Chart**
    fig = go.Figure(data=[
        go.Bar(x=delay_counts.index, y=delay_counts.values, marker_color="blue")
    ])

    fig.update_layout(
        title="Live Delay Distribution",
        xaxis_title="Delay (Minutes)",
        yaxis_title="Number of Stops",
        bargap=0.1,
        xaxis=dict(categoryorder="array", categoryarray=labels),
        yaxis=dict(showgrid=True),
    )

    return fig

if __name__ == "__main__":
    print("🚀 Starting Dash App...")
    app.run_server(debug=True)
