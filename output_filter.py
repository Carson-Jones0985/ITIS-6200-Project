SUSPICIOUS_OUTPUTS = ["i cannot help with that", "ignore all previous instructions", "ignore previous instructions" "as an ai, i must", "my new instructions", "i have been told to", "the system has been hacked",]

def filter_output(response):
    lower = response.lower()
    for phrase in SUSPICIOUS_OUTPUTS:
        if phrase in lower:
            return None, f"Suspicious output detected: '{phrase}' found in response."
    return response, None