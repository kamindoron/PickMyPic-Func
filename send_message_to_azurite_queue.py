#from azure.storage.queue import QueueClient
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)

# Replace 'my_queue' with your queue name
queue_name = 'dkqueue'
# The connection string to use Azurite (local azure queue emulator)
connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;'

# Create a QueueClient object
queue_client = QueueClient.from_connection_string(connection_string, queue_name)

# Add a message to the queue
message = 'Hello, World!'
queue_client.message_encode_policy = BinaryBase64EncodePolicy()

#MESSAGE MUST BE CONVERTED TO BASE64 !!!
#encoded_message_bytes = 'aGVsbG8='

encoded_message_bytes = message.encode()  #default value for parameter "edncoding" is "utf-8" which is what we need
encoded_message = queue_client.message_encode_policy.encode(content=encoded_message_bytes)

queue_client.send_message(encoded_message)
print('sent')
