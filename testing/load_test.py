from locust import FastHttpUser, HttpUser, task, between


class UserBehavior(FastHttpUser):
    wait_time = between(1, 3)

    @task
    def get_trains(self):
        self.client.get("/api/trains/")

    @task
    def book_seat(self):
        self.client.post("/api/book-seat/", data={"user_id": 1})
