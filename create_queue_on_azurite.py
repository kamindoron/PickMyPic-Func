from azure.storage.queue import QueueServiceClient

# The connection string to use Azurite
connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;'

# Create a QueueServiceClient object
service_client = QueueServiceClient.from_connection_string(connection_string)

# Name of the queue
queue_name = "dkqueue2"

# Create the queue
service_client.create_queue(queue_name)