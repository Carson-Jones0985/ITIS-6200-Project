INJECTION_PHRASES = ["ignore previous instructions", "ignore all previous", "forget everything", "disregard", "set aside your earlier guidance", "do not follow", "override", "from now on", "pretend you are", "you are now", "act as",]

def sanitize_chunks(chunks):
    cleaned = []
    flagged = []
    
    for chunk in chunks:
        lower = chunk.lower()
        chunk_flagged = False
        for phrase in INJECTION_PHRASES:
            if phrase in lower:
                chunk_flagged = True
                break
        if chunk_flagged:
            flagged.append(chunk)
        else:
            cleaned.append(chunk)
    
    return cleaned, flagged