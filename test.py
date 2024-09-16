data = [
    {
        "message": "Data has been loaded successfully.",
        "timestamp": "2024-05-07T07:20:17.245582+00:00"
    },
    {
        "message": "Data cleaning has been done.",
        "timestamp": "2024-05-07T07:20:17.401493+00:00"
    },
    {
        "message": "Exploratory data analysis has been done.",
        "timestamp": "2024-05-07T07:20:28.208139+00:00"
    },
    {
        "message": "Variables Correlation Analysis has been done.",
        "timestamp": "2024-05-07T07:20:29.869966+00:00"
    },
    {
        "message": "Data transformation has been done.",
        "timestamp": "2024-05-07T07:20:29.892019+00:00"
    },
    {
        "message": "Modeling has been done.",
        "timestamp": "2024-05-07T07:20:41.889550+00:00"
    },
    {
        "message": "Analysis report has been generated.",
        "timestamp": "2024-05-07T07:22:12.225224+00:00"
    },
    {
        "message": "Data analysis knowledge of this file has been transferred to chatbot.",
        "timestamp": "2024-05-07T07:22:12.251161+00:00"
    }
]

# Create a list of formatted strings containing the message and timestamp
formatted_messages = [f"{entry['message']} {entry['timestamp']}" for entry in data]

# Print each formatted message on a new line
for message in formatted_messages:
    print(message)
