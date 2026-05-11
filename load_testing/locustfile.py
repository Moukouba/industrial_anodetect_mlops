from locust import HttpUser, task, between
import os

class FastAPIUser(HttpUser):
    wait_time = between(1, 2)  # Users will wait between 1 and 2 seconds between tasks

    @task(3)  # This task will be executed 3 times more often than the health check
    def predict_endpoint(self):
        # Ensure the sample image exists
        image_path = "load_testing/sample_image.png"
        if not os.path.exists(image_path):
            print(f"Error: Sample image not found at {image_path}")
            return

        with open(image_path, "rb") as image_file:
            files = {"file": ("sample_image.png", image_file, "image/png")}
            self.client.post("/predict", files=files, name="/predict [POST]")

    @task(1)
    def health_check(self):
        self.client.get("/health", name="/health [GET]")
        
        
# locust -f load_testing/locustfile.py
