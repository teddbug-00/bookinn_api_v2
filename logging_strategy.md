# BookInn API Logging Strategy Guide

## Table of Contents
1. [General Logging Format](#general-logging-format)
2. [Core Components Logging](#core-components-logging)
3. [Implementation Details](#implementation-details)
4. [Directory Structure](#directory-structure)
5. [Environment Configuration](#environment-configuration)

## General Logging Format
```python
log_format = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
```

## Core Components Logging

### Authentication & Security
#### Login Events
```python
# Successful login
logger.info(f"User {user_id} logged in successfully")

# Failed login
logger.warning(f"Failed login attempt for email {masked_email}")

# Token operations
logger.info(f"Token refresh for user {user_id}")
logger.warning(f"Multiple failed login attempts for email {masked_email}")
```

### User Management
#### Registration & Profile Events
```python
# New registrations
logger.info(f"New user registered: {user_id}")

# Profile updates
logger.info(f"Profile updated for user {user_id}: fields={updated_fields}")
logger.info(f"Profile picture changed for user {user_id}")
```

### Property Listings
#### Listing Management
```python
# Creation and modifications
logger.info(f"New listing created: {listing_id} by user {owner_id}")
logger.info(f"Listing {listing_id} updated: fields={modified_fields}")
logger.info(f"Listing {listing_id} deleted by user {user_id}")

# Interactions
logger.info(f"Listing {listing_id} viewed by user {user_id}")
logger.info(f"Search query: {search_params} by user {user_id}")
```

### Reviews & Ratings
```python
logger.info(f"New review {review_id} added for listing {listing_id} by user {user_id}")
logger.info(f"Review {review_id} updated by user {user_id}")
```

### Performance Monitoring
```python
# Database performance
logger.warning(f"Slow query detected: {query_details} - execution time: {execution_time}ms")
logger.error(f"Database operation failed: {error_details}")

# API performance
logger.info(f"API Response Time - Endpoint: {endpoint} - Duration: {duration}ms")
```

## Implementation Details

### Custom Logger Class
```python
class APILogger:
    def __init__(self):
        self.logger = logging.getLogger('bookinn_api')
        self.setup_logger()

    def setup_logger(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        )
        
        # File handler for all logs
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Error logs handler
        error_handler = logging.FileHandler('logs/error.log')
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # Development console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)
```

### Request Logging Middleware
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.2f}s"
    )
    
    return response
```

### Log Rotation Configuration
```python
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5
)
```

## Directory Structure
```
logs/
├── app.log           # General application logs
├── error.log         # Error-level logs only
├── security.log      # Security-related events
├── performance.log   # Performance metrics
└── audit.log        # User action audit trail
```

## Environment Configuration
```python
# Log levels per environment
LOG_LEVEL = {
    'development': logging.DEBUG,
    'staging': logging.INFO,
    'production': logging.WARNING
}

# Environment-specific settings
LOGGING_CONFIG = {
    'development': {
        'handlers': ['console', 'file'],
        'format': 'detailed'
    },
    'production': {
        'handlers': ['file'],
        'format': 'minimal'
    }
}
```

## Best Practices

1. **Sensitive Data**
   - Never log passwords, tokens, or personal information
   - Mask sensitive data like email addresses
   - Use appropriate log levels

2. **Performance**
   - Implement log rotation
   - Regular log cleanup
   - Monitor log file sizes

3. **Security**
   - Secure log file permissions
   - Regular log analysis for security events
   - Implement log backup strategy

4. **Maintenance**
   - Regular log analysis
   - Monitor disk space
   - Archive old logs
   - Set up log alerts

## Implementation Steps

1. Create logging directory structure
```bash
mkdir logs
```

2. Add logging configuration to your FastAPI app
```python
from fastapi import FastAPI
from .logging import APILogger

app = FastAPI()
logger = APILogger().logger
```

3. Add middleware to main.py
```python
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # ... middleware code from above ...
```

4. Set up log rotation using Windows Task Scheduler
```powershell
# PowerShell script for log rotation
Get-ChildItem "logs\*.log" | Where-Object {
    $_.LastWriteTime -lt (Get-Date).AddDays(-30)
} | Remove-Item
```

## Monitoring Tools Integration

### ELK Stack Configuration
```yaml
input {
  file {
    path => "c:/Users/dickson/Documents/learning_fastapi/logs/*.log"
    type => "bookinn_logs"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{LOGLEVEL:log_level} - %{WORD:module} - %{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "bookinn-logs-%{+YYYY.MM.dd}"
  }
}
```

## Simplified Data Masking with Python Packages

### 1. Using `mask-utils`
```bash
pip install mask-utils
```

```python
from mask_utils import mask

# Simple usage
masked_email = mask.email("john.doe@example.com")  # j***@example.com
masked_phone = mask.phone("123-456-7890")         # ***-***-7890
masked_card = mask.card("4532015112830366")       # ************0366

# In your logging code
logger.info(f"Login attempt for: {mask.email(user_email)}")
```

### 2. Using `python-mask`
```bash
pip install python-mask
```

```python
from python_mask import mask_string

# Configure masking patterns
MASK_PATTERNS = {
    'email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
    'phone': r'\d{3}[-.]?\d{3}[-.]?\d{4}',
    'ssn': r'\d{3}-\d{2}-\d{4}'
}

# Create a masking middleware
class MaskingMiddleware:
    def __init__(self, app, patterns=MASK_PATTERNS):
        self.app = app
        self.patterns = patterns

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def masked_receive():
            message = await receive()
            if message.get("type") == "http.request":
                # Mask sensitive data in request body
                body = message.get("body", b"").decode()
                for pattern in self.patterns.values():
                    body = mask_string(body, pattern)
                message["body"] = body.encode()
            return message

        await self.app(scope, masked_receive, send)

# Add to your FastAPI app
app.add_middleware(MaskingMiddleware)
```

### 3. Using `scrubadub` (Most Comprehensive)
```bash
pip install scrubadub
```

```python
import scrubadub

class SensitiveDataFilter:
    def __init__(self):
        self.scrubber = scrubadub.Scrubber()
        # Add specific detectors as needed
        self.scrubber.add_detector(scrubadub.detectors.email.EmailDetector)
        self.scrubber.add_detector(scrubadub.detectors.phone.PhoneDetector)
        self.scrubber.add_detector(scrubadub.detectors.credit_card.CreditCardDetector)

    def clean(self, text: str) -> str:
        return self.scrubber.clean(text)

# Usage in your logging setup
data_filter = SensitiveDataFilter()

class SecureLogger:
    def __init__(self):
        self.logger = logging.getLogger('secure_logger')
        self.data_filter = SensitiveDataFilter()

    def info(self, message: str):
        clean_message = self.data_filter.clean(message)
        self.logger.info(clean_message)

# Example usage
secure_logger = SecureLogger()
secure_logger.info(f"Processing payment for {email} with card {card_number}")
# Output: Processing payment for {{EMAIL}} with card {{CREDIT_CARD}}
```

### 4. Automatic Integration with FastAPI

```python
from fastapi import FastAPI, Request
from scrubadub import Scrubber
from functools import partial

app = FastAPI()
scrubber = Scrubber()

class SecureRequestMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        
        # Clean the response data
        if hasattr(response, 'body'):
            clean_body = scrubber.clean(response.body.decode())
            response.body = clean_body.encode()
            
        return response

# Add the middleware to your FastAPI app
app.add_middleware(SecureRequestMiddleware)
```

These packages offer different levels of functionality:
- `mask-utils`: Simple, lightweight, good for basic masking needs
- `python-mask`: More flexible, pattern-based masking
- `scrubadub`: Most comprehensive, with built-in detectors for various types of sensitive data

Choose based on your needs:
- For basic masking: Use `mask-utils`
- For custom patterns: Use `python-mask`
- For comprehensive data detection and cleaning: Use `scrubadub`