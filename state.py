from upstash_redis import Redis

redis = Redis.from_env()

STATE_KEY = "alert:sent"


def has_alert_been_sent():
    return redis.get(STATE_KEY) == "1"


def set_alert_state(is_sent: bool):
    state = 1 if is_sent else 0
    redis.set(STATE_KEY, state)
