from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    host = "http://localhost:5000" 

    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        
        if not self.token: 
            raise ValueError("Login failed: Token not found in cookies.")
        
        self.default_headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Cookies": f"token:{self.token}",
        }

    @task
    def t(self):
        headers = {
            **self.default_headers,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Host": "localhost:5000",
            "Priority": "u=0, i",
            "Referer": "http://localhost:5000/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        with self.client.request(
            "GET", "/cart", headers=headers, catch_response=True
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Request failed with status code {resp.status_code}")

if __name__ == "__main__":
    run_single_user(AddToCart)
