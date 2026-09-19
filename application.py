from dataclasses import dataclass
from typing import Optional

@dataclass
class Application:
    company: str
    role: str
    location: str
    application_date: str
    job_link: Optional[str]
    status: str
