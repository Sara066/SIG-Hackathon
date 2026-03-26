from dataclasses import dataclass

@dataclass
class AlertEvent:
    name: str
    status: str
    memory_mb: float
    is_anomaly: bool = False