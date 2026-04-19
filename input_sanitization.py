INJECTION_PHRASES = ["ignore previous instructions", "ignore all previous", "forget everything", "disregard", "set aside your earlier guidance", "do not follow", "override", "from now on", "pretend you are", "you are now", "act as",]

def sanitize_chunks(chunks):
    cleaned = []
    flagged = []
    
    for chunk in chunks:
        chunk_flagged = False
        cleaned_lines = []

        for line in chunk.split("\n"):
            lower = line.lower()
            line_flagged = False
            for phrase in INJECTION_PHRASES:
                if phrase in lower:
                    line_flagged = True
                    chunk_flagged = True
                    break
            if not line_flagged:
                cleaned_lines.append(line)

        if chunk_flagged:
            flagged.append(chunk)

        cleaned.append("\n".join(cleaned_lines))

    return cleaned, flagged