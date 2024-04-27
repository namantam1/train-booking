from locust import HttpUser, task, between
from random import choice
import json

with open("data.json", "r") as fp:
    data = json.load(fp)

def get_data():
    train = choice(data)
    stops = train["stops"]
    count = int(len(stops) / 2)
    source = choice(stops[:count])
    destination = choice(stops[count:])
    train = train["train"]
    return train, source, destination


class UserBehavior(HttpUser):
    wait_time = between(1, 3)

    @task(10)
    def get_trains(self):
        _, source, destination = get_data()
        self.client.get("/api/trains/", params={
            "source": source,
            "destination": destination
        })

    @task(1)
    def book_seat(self):
        train, source, destination = get_data()
        self.client.post("/api/book-seat/", data={
            "train": train,
            "source": source,
            "destination": destination
        })
