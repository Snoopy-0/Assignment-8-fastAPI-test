import threading, time, socket
import uvicorn
from module8_is601.main import app
import pytest
from playwright.sync_api import sync_playwright

def free_port(start=8000):
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
    # Wait for server
    time.sleep(1.0)
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