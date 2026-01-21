from datetime import datetime, timedelta
import time

class LongPoller:
    
    def __init__(self, message_service, timeout=25, interval=0.5):
        self.message_service = message_service
        self.timeout = timeout
        self.interval = interval

    def wait_for_new_messages(self, after_timestamp: datetime):
        start = datetime.now()

        while datetime.now() - start < timedelta(seconds=self.timeout):
            new_messages = self.message_service.get_messages_after(after_timestamp)
            if new_messages:
                return [m.to_dict() for m in new_messages]
            time.sleep(self.interval)

        return []  



