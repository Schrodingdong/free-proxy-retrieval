import requests
from multiprocessing.pool import ThreadPool

PROXYSCRAPE_URL = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=protocolipport&format=text&timeout=5215"
THREAD_NUMBER = 20


def format_proxies(proxies):
    formated_proxies = list(
            map(lambda p: {"http": p.strip(), "https": p.strip(), "no_proxy": None}, proxies)
    )
    return formated_proxies


def check_proxy_worker(proxy):
    try:
        res = requests.get("https://api.ipify.org?format=json",
                           proxies=proxy,
                           timeout=3
                           )
        if res.status_code == 200:
            working_proxy = proxy["http"]
            print(f"found: {working_proxy}")
            return working_proxy
    except Exception:
        return None


def check_proxies(proxies: list):
    working_proxies = []
    pool = ThreadPool(processes=THREAD_NUMBER)
    for working_proxy in pool.map(check_proxy_worker, proxies):
        if working_proxy is not None:
            working_proxies.append(working_proxy)
    return working_proxies


def save_working_proxies(working_proxies: list):
    with open("working_proxies.txt", "w") as f:
        for wp in working_proxies:
            f.writelines(wp + "\n")


def load_proxies():
    proxies_text = requests.get(PROXYSCRAPE_URL).text
    proxies = proxies_text.splitlines()
    return format_proxies(proxies)


def main():
    proxies = load_proxies()
    working_proxies = check_proxies(proxies)
    save_working_proxies(working_proxies)


if __name__ == "__main__":
    main()
