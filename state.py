from upstash_redis import Redis

try:
    redis = Redis.from_env()
except Exception:
    redis = None
    print("Upstash Redis is not configured. Skipping alert state tracking.")

STATE_KEY = "alert:sent"


def has_alert_been_sent():
    if not redis:
        return False

    return redis.get(STATE_KEY) == "1"


def set_alert_state(is_sent: bool):
    if not redis:
        return

    state = 1 if is_sent else 0
    redis.set(STATE_KEY, state)
