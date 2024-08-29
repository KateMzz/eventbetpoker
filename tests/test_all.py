import pytest
import uuid
from playwright.sync_api import sync_playwright

HOME_URL = "https://poker.evenbetpoker.com/html5-evenbetpoker/d/?tables/all"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def new_page(browser):
    """create and cleanup the browser context and page"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


def wait_for_page_load(page):
    """Handle the initial page loading and waiting for the spinner to disappear"""
    page.goto(HOME_URL, timeout=60000)
    page.wait_for_function('document.querySelector("#root-spinner") === null', timeout=120000)


def open_first_game(page):
    """Navigate to the Casino section and open the first game"""
    page.get_by_text("Casino").click()
    page.wait_for_selector(".WidgetCasinoGameListContainer__content", timeout=30000)
    element = page.locator('.WidgetCasinoGameListItemContainer__content').nth(0)
    element.hover()
    element.click()
    page.wait_for_selector(".WidgetCasinoGameListGamesPlayerContainer__games__wrapper.games_1", timeout=30000)


def test_registration_and_open_game(new_page):
    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f'{username}@gmail.com'
    password = 'strongpass'

    page = new_page
    wait_for_page_load(page)
    page.get_by_text("Sign up").click(force=True)
    page.locator('input:near(span:text("Nickname"))').fill(username)
    page.locator('input[type="email"]').fill(email)
    page.locator('input[type="password"]').nth(0).fill(password)
    page.locator('input[type="password"]').nth(1).fill(password)
    page.get_by_text("Send").click(force=True)
    page.wait_for_selector(".LobbyMiniUserInfoContainer__user_info .MiniUserInfo__nickname_text", timeout=30000)
    assert page.locator(
        ".panel.MiniUserInfo__nickname_text").inner_text() == username, "Registration failed or username mismatch"

    # Step 2: Open Casino and Launch the first game
    open_first_game(page)


def test_login_and_open_game(new_page):
    username = 'example1'
    password = '12345678!'

    page = new_page
    wait_for_page_load(page)
    page.get_by_text("Login").click(force=True)
    page.locator('input[name="username"]').fill(username)
    page.locator('input[name="password"]').fill(password)
    page.locator('text=Login').nth(2).click(force=True)
    page.wait_for_selector(".LobbyMiniUserInfoContainer__user_info .MiniUserInfo__nickname_text", timeout=30000)
    assert page.locator(
        ".panel.MiniUserInfo__nickname_text").inner_text() == username, "Registration failed or username mismatch"

    # Step 2: Open Casino and Launch the first game
    open_first_game(page)


def test_open_game_unauthorized(new_page):
    page = new_page
    wait_for_page_load(page)

    # Step 2: Open Casino and Launch the first game
    open_first_game(page)
