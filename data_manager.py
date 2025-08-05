import json
import os

DATA_FILE = 'data.json'

class DataManager:
    def __init__(self):
        if not os.path.exists(DATA_FILE):
            self.data = {}
            self.save()
        else:
            with open(DATA_FILE, 'r') as f:
                self.data = json.load(f)

    def save(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_machine(self, machine_name):
        if machine_name not in self.data:
            self.data[machine_name] = {}

    def add_record(self, machine_name, date, record):
        self.add_machine(machine_name)
        if date not in self.data[machine_name]:
            self.data[machine_name][date] = []
        self.data[machine_name][date].append(record)
        self.save()

    def get_records(self, machine_name, date):
        return self.data.get(machine_name, {}).get(date, [])

    def get_machines(self):
        return list(self.data.keys())

    def get_dates(self, machine_name):
        return list(self.data.get(machine_name, {}).keys())