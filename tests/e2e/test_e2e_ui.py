import threading, time, socket
import uvicorn
import pytest
from playwright.sync_api import sync_playwright
from main import app  

def free_port():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

@pytest.fixture(scope="session")
def live_server():
    port = free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(1.0)  # wait for server
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=1.0)

def test_ui_addition(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(live_server + "/")
        page.fill("#a", "2")
        page.fill("#b", "3")
        page.select_option("#op", "add")
        page.click("text=Calculate")
        page.wait_for_selector("#out")
        assert "Result: 5" in page.inner_text("#out")
        browser.close()
