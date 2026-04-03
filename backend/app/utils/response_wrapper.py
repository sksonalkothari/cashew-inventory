from datetime import datetime

def wrap_response(data):
    return {
        "data": data,
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }