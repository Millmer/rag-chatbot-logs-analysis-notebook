import json
import random
import string
import datetime
from dataclasses import dataclass
from typing import Optional
from user_agent import generate_user_agent

@dataclass
class LogEntry:
    ip: str
    chat_id: str
    user_agent: str
    timestamp: Optional[str] = None
    event_type: Optional[str] = None
    content: Optional[str] = None
    processing_times: Optional[str] = None

    def __str__(self) -> str:
        """Returns a string representing a log entry"""
        return f"{self.ip} - [{self.timestamp}] \"SOCKET.IO {self.event_type}\" - \"{self.user_agent}\" - Event({self.chat_id}): {self.content}{self.processing_times}"

def load_questions(file_path):
    with open(file_path, 'r') as file:
        questions = file.readlines()
    # Strip newline characters and any leading/trailing whitespace
    questions = [q.strip() for q in questions]
    return questions

def generate_ip():
    """Generate a random IP address."""
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def generate_timestamp():
    """Generate a timestamp with current date and time, slightly varied."""
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = datetime.timedelta(seconds=random.randint(-60, 60))
    return (now + delta).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def generate_random_alphanumeric(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def update_log_entry(log_entry: LogEntry, event_type, content):
    processing_times = ""
    if (event_type == "chat:ask" and not (content == '"[START]"' or content == '"[END]"')): processing_times = generate_processing_times()
    if not log_entry.timestamp:
        log_entry.timestamp = generate_timestamp()
    else:
        delta = datetime.timedelta(seconds=random.randint(1, 60))
        log_entry.timestamp = (datetime.datetime.strptime(log_entry.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + delta).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    timestamp = generate_timestamp()
    log_entry.timestamp = timestamp
    log_entry.event_type = event_type
    log_entry.content = content
    log_entry.processing_times = processing_times
    return log_entry

def generate_chat_session():
    logs = []
    chat_id = generate_random_alphanumeric()
    ip = generate_ip()
    user_agent = generate_user_agent()

    entry = LogEntry(ip=ip, chat_id=chat_id, user_agent=user_agent)

    # Start a chat session
    entry = update_log_entry(entry, "chat:create", f'"{chat_id}"')
    logs.append(str(entry))

    # Add a few chat:ask and chat:speak events
    num_messages = random.randint(1, 5)  # Random number of messages in a chat
    for _ in range(num_messages):
        logs.append(str(update_log_entry(entry, "chat:ask", '"[START]"')))
        question = random.choice(questions)
        logs.append(str(update_log_entry(entry, "chat:ask", f'{{"role":"user","content":{json.dumps(question)}}}')))
        logs.append(str(update_log_entry(entry, "chat:ask", '"[END]"')))
        # Optionally add a chat:speak event
        if random.choice([True, False]):
            logs.append(str(update_log_entry(entry, "chat:speak", f'"{chat_id}"')))

    # End the chat session
    logs.append(str(update_log_entry(entry, "chat:ask", '"[START]"')))

    return logs

def generate_processing_times():
    """Generate random processing times for different stages."""
    stages = ["\nModerating", "Embedding", "Fetching Sources", "Tokenising Sources", "Answering"]
    return "\n".join(f"{stage} ({random.randint(100, 1000)}ms)" for stage in stages)

def save_logs_to_file(logs, filename):
    with open(filename, 'w') as file:
        for log in logs:
            file.write(log + '\n')


num_logs = 100
chat_session_logs = []
questions = load_questions('./questions.txt')

for _ in range(num_logs):
    chat_session_logs.extend(generate_chat_session())

print(chat_session_logs[:5])

save_logs_to_file(chat_session_logs, 'example-logs.log')
