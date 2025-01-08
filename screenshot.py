import datetime
import os
import pyautogui


def take_screenshot() -> None:
    time: datetime.datetime = datetime.datetime.now()
    formatted_time: str = datetime.datetime.strftime(time, format="%m.%d.%y.%I.%M.%S") + '.png'

    # Locate the path to the current project
    project_path: str = os.path.dirname(__file__)

    # Create screenshot path
    screenshot: str = os.path.join(project_path, formatted_time)
    
    pyautogui.screenshot(screenshot)
