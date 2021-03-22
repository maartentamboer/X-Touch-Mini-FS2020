

class MockSimconnect:
    pass
    def map_to_sim_event(self, value):
        print('MockSimconnect::map_to_sim_event', value)

    def send_event(self, event, value):
        print('MockSimconnect::send_event', event, value)

class MockEvent:
    def __init__(self, key):
        self._key = key

    def __call__(self, value=0):
        print('MockEvent::__call__', self._key, value)


class MockAircraftEvents:
    def __init__(self):
        self.sm = MockSimconnect()

    @staticmethod
    def find(key):
        return MockEvent(key)


class MockAircraftRequests:
    def __init__(self):
        self.sm = MockSimconnect()
        self.list = []

    @staticmethod
    def get(key):
        # print('MockAircraftRequests::get', key)
        return 0

    @staticmethod
    def set(key, value):
        print('MockAircraftRequests::set', key, value)
        return True
