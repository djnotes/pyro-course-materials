import threading
import time
import uuid
import pika
import json

class WorkManager:
    def __init__(self, rabbitmq_url='amqp://guest:guest@localhost/', queue_name='ffmpeg_tasks'):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.tasks = {}  # task_id -> {'status': ..., 'start_time': ..., ...}
        self.lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.producer_thread = threading.Thread(target=self._producer, daemon=True)
        self._stop_event = threading.Event()
        self.worker_thread.start()
        self.producer_thread.start()

    def addTask(self, task_data):
        task_id = str(uuid.uuid4())
        with self.lock:
            self.tasks[task_id] = {'status': 'queued', 'start_time': None, 'data': task_data}
        self._send_to_queue(task_id, task_data)
        return task_id

    def checkQueue(self):
        with self.lock:
            return any(task['status'] == 'queued' for task in self.tasks.values())

    def checkQueueLoad(self):
        with self.lock:
            return sum(1 for task in self.tasks.values() if task['status'] == 'queued')

    def checkQueueHealth(self, timeout=300):
        now = time.time()
        with self.lock:
            for task_id, task in self.tasks.items():
                if task['status'] == 'processing' and task['start_time'] and (now - task['start_time'] > timeout):
                    return False
        return True

    def removeTask(self, task_id):
        with self.lock:
            if task_id in self.tasks and self.tasks[task_id]['status'] == 'queued':
                self.tasks[task_id]['status'] = 'cancelled'
                return True
        return False

    def checkTaskStatus(self, task_id):
        with self.lock:
            return self.tasks.get(task_id, {}).get('status', 'not_found')

    def _send_to_queue(self, task_id, task_data):
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        message = json.dumps({'task_id': task_id, 'data': task_data})
        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()

    def _producer(self):
        # This can be extended for periodic or batch task production
        while not self._stop_event.is_set():
            time.sleep(1)

    def _worker(self):
        def callback(ch, method, properties, body):
            msg = json.loads(body)
            task_id = msg['task_id']
            with self.lock:
                if self.tasks.get(task_id, {}).get('status') == 'cancelled':
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                self.tasks[task_id]['status'] = 'processing'
                self.tasks[task_id]['start_time'] = time.time()
            # Simulate ffmpeg processing
            time.sleep(2)  # Replace with actual ffmpeg call
            with self.lock:
                self.tasks[task_id]['status'] = 'completed'
            ch.basic_ack(delivery_tag=method.delivery_tag)

        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        channel.start_consuming()

    def stop(self):
        self._stop_event.set()