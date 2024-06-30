from azure.storage.queue import QueueClient

# Replace with your Azurite connection string and queue name
#connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFQq2UVErCz9Rk8LO0AMWKn5GJy9RTo6ZD3jl2A==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;'
queue_name = "dkqueue"

# Create a QueueClient object
queue_client = QueueClient.from_connection_string(connection_string, queue_name)

# Receive messages from the queue
messages = queue_client.receive_messages()
print(messages)

for message in messages:
    # Process the message (optional)
    print(f"Processing message: {message.content}")

    # Delete the message from the queue
    queue_client.delete_message(message.id, message.pop_receipt)
