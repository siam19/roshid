from upstash_redis import Redis

redis = Redis(url="https://destined-hare-44940.upstash.io", token="Aa-MAAIjcDE5YTJkNDJiMTg0NTM0MTZmOWE0MmUzZTczZDUzNDIzZHAxMA")

redis.set("eet", "patkel")
value = redis.get("eet")


print(value)  