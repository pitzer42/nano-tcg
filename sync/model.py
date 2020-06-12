class Model:

    def __init__(self):
        self.state = 0
        self.observers = list()

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.notify(self.state)

    def change_state(self):
        self.state += 1
        self.notify_observers()