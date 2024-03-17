from playwright.sync_api import sync_playwright
import time

def enter_daily_tasks(login, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Anuko Timetracker
        page.goto("https://timetracker.inthergroup.com")

        # Login
        page.fill('input[name="login"]', login)
        page.fill('input[name="password"]', password)
        page.click('input[name="btn_login"]')

        page.wait_for_load_state()

        page.goto("https://timetracker.inthergroup.com/time.php")
        submit_today = input("Do you want to submit this record for today? (yes/no): ")
        if submit_today.lower() == "no":
            date_to_record = input("Enter the date to record for (yyyy-mm-dd): ")
            page.goto(f"https://timetracker.inthergroup.com/time.php?date={date_to_record}")

        page.wait_for_selector('select[name="project"]:enabled')

        project_name = input("Enter a piece of the project name: ")

        page.click('select[name="project"]')

        # tis to wait for the dropdown options to load
        time.sleep(1)

        # all the project options
        project_options = page.query_selector_all('select[name="project"] option')

        for option in project_options:
            option_text = option.evaluate('(element) => element.textContent')
            if option_text and project_name.lower() in option_text.lower():
                project_value = option.get_attribute('value')
                # Select the option
                page.select_option('select[name="project"]', value=project_value)
                page.click('body')
                break
        else:
            print("Project not found.")
            browser.close()
            return

        page.wait_for_selector('select[name="task"]:enabled')

        task_name = input("Enter a piece of the task name: ")

        task_options = page.query_selector_all('select[name="task"] option')

        for option in task_options:
            option_text = option.evaluate('(element) => element.textContent')
            if option_text and task_name.lower() in option_text.lower():
                task_value = option.get_attribute('value')
                # Select the option
                page.select_option('select[name="task"]', value=task_value)
                page.click('body')
                break
        else:
            print("Task not found.")
            browser.close()
            return

        duration = input("Enter the duration of the task (HH:MM): ")
        page.fill('input[name="duration"]', duration)

        note = input("Enter a note for the task: ")
        page.fill('textarea[name="note"]', note)

        page.click('input[name="btn_submit"]')
        print("Task submitted successfully.")
        input("Press any key to continue...")

def read_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        credentials = {}
        for line in lines:
            key, value = line.strip().split('=')
            credentials[key.strip()] = value.strip()
        return credentials.get('login'), credentials.get('password')


login, password = read_credentials("credentials.txt")

enter_daily_tasks(login, password)