from playwright.sync_api import sync_playwright
import time

def read_notes():
    try:
        with open("notes.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_notes(notes):
    with open("notes.txt", "w") as file:
        file.writelines(notes)
        file.close()

def search_note_in_file(note):
    notes = read_notes()
    for line in notes:
        if note in line:
            return line.strip()
    return None

def add_note_to_file(new_note):
    notes = read_notes()
    notes.append(new_note + "\n")
    write_notes(notes)

def delete_note_from_file(note):
    notes = read_notes()
    updated_notes = [line for line in notes if note not in line]
    write_notes(updated_notes)

def input_note():
    while True:
        note = input("Enter a piece of the note: ")
        found_note = search_note_in_file(note)
        if found_note:
            print("Note found:", found_note)
            delete_option = input("Do you want to delete this note from notes.txt? (yes/no): ")
            if delete_option.lower() == "yes":
                delete_note_from_file(found_note)
                print("Note deleted from notes.txt.")
            return found_note
        else:
            print("This note was not found in notes.txt.")
            add_option = input("Do you want to add this note to notes.txt? (yes/no): ")
            if add_option.lower() == "yes":
                add_note_to_file(note)
                print("Note added to notes.txt.")
            return note
def enter_daily_tasks(login, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://timetracker.inthergroup.com")

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
                page.select_option('select[name="task"]', value=task_value)
                page.click('body')
                break
        else:
            print("Task not found.")
            browser.close()
            return

        duration = input("Enter the duration of the task (HH:MM): ")
        page.fill('input[name="duration"]', duration)

        note = input_note()
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