from dataclasses import dataclass
from datetime import datetime

@dataclass
class Log:
    message: str
    timestamp: float
    display_time: str

    @staticmethod
    def create(message: str):
        now = datetime.now()
        return Log(
            message=message,
            timestamp=now.timestamp(),
            display_time=now.strftime("%H:%M:%S")
        )