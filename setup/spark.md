## Setup Spark Cluster

![spark](../documentation/spark.jpg)

We will start the Spark Streaming process in the DataProc cluster we created to communicate with the Kafka VM instance over the port `9092`. Remember, we opened port 9092 for it to be able to accept connections.

- Establish SSH connection to the **master node**

  ```bash
  ssh streamify-spark
  
- Clone git repo

  ```bash
  git clone https://github.com/ilhamaulanap/streamcommerce.git && \
  cd streamcommerce/spark_streaming
  ```

- Start reading messages

  ```bash
nohup spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 \
    stream.py \
> nohup.out 2>&1 &
  ```

- If all went right, you should see new `parquet` files in your bucket! That is Spark writing a file every two minutes for each topic.

- Topics we are reading from

  - feedback
  - page_view_events
  - traffic
  - transactions
  - views