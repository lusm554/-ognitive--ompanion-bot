import os, time
import requests

token = os.getenv("TELEGRAM_TOKEN")
url = f"https://api.telegram.org/bot{token}/getMe"

el_times = []
for i in range(10):
  res = requests.get(url)
  elapsed = res.elapsed.total_seconds()
  print("Request done in", elapsed, "s")
  el_times.append(float(elapsed))
  time.sleep(3) 

avg = sum(el_times)/len(el_times)
print("Average response time in 10 requests", avg)
