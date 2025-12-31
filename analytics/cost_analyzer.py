import json

PRICE = 0.0005
total = 0

with open("logs/geoplant.json.log") as f:
    for line in f:
        log = json.loads(line)
        if log.get("event") == "llm_call":
            total += log["total_tokens"]

print("Tokens:", total)
print("Cost ($):", round((total/1000)*PRICE, 4))
