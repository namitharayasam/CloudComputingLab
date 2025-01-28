from locust import task, run_single_user
from locust import FastHttpUser


class Browse(FastHttpUser):
    host = "http://localhost:5000"
   
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        headers = self.default_headers.copy()
        headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
        })
       
        with self.client.request(
            "GET",
            "/browse",
            headers=headers,
            catch_response=True,
        ) as resp:
            pass
       
if __name__ == "__main__":
    run_single_user(Browse)
