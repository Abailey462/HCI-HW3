from django.forms.widgets import Textarea
from nicegui import ui
import requests

API_URL = "http://localhost:8005"

questions = []

with ui.element('div').classes('w-full flex items-center justify-center bg-transparent').style('height: 200px;'):
    ui.label("HCI Review Application").classes("text-5xl font-bold")

ui.query('body').style('background-color: var(--q-primary);')
page_body_row = ui.row()
page_body_col = ui.column().classes("border 2px, padding 2rem;")
def api_get(path):
    try:
        # Attempt to send GET request to API
        response = requests.get(f"{API_URL}{path}", timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, GET was successful so return response data
        return response.json()
    except requests.RequestException as e:
        # GET request was unsuccessful
        # Send an alert with error details to the UI and return empty list
        ui.notify(f"Could not reach API: {e}", type="negative")
        return []

def api_post(path, data):
    try:
        # Attempt to send POST request to API with data payload
        response = requests.post(f"{API_URL}{path}", json=data, timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, POST was successful so return True
        return True
    except requests.RequestException as e:
        # POST request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

def api_delete(path, id) -> bool:
    """Send delete request to API for object with given id.

    Args:
        path: The path of the endpoint to send a delete to.
        id: The id of the desired object to delete.
    Returns:
        Wether the delete was successful.
    """
    try:
        # Attempt to send DELETE request to API with data payload
        response = requests.delete(f"{API_URL}{path}/{id}", timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, DELETE was successful so return True
        return True
    except requests.RequestException as e:
        # DELETE request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

def api_put(path, id, data) -> bool:
    """Send PUT request to API for object with `id`

    Args:
        path: The path of the endpoint to send a delete to.
        id: The id of the desired object to delete.
        data: The data to update a given object with.
    Returns:
        Wether the PUT was successful.
    """
    try:
        # Attempt to send PUT request to API with data payload
        response = requests.put(f"{API_URL}{path}/{id}", json=data, timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, PUT was successful so return True
        return True
    except requests.RequestException as e:
        # PUT request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

def render_question(question):
    with ui.card().style('min-width: 200px; flex: 0 0 auto;') as card:
            card.on("click", lambda: toggle_answer(question["id"]))
            ui.label(question["q"])
            ui.label(question["a"]).classes("text-s text-green font-bold").bind_visibility_from(question["state"], "show_answer")

            with ui.dialog() as dialog, ui.card().classes("w-full"):
                ui.label("Question")
                new_q = ui.textarea(label=question["q"]).classes("w-full")
                ui.label("Answer")
                new_a = ui.textarea(label=question["a"]).classes("w-full")
                ui.button('Update question', on_click=lambda: update_question(
                    "/update", question["id"], new_q.value, new_a.value, dialog
                ))

            with ui.row():
                ui.button(text="Delete", on_click=lambda: delete_question(path="/delete", id=question["id"])).on('click.stop')
                ui.button('Edit', on_click=dialog.open).on('click.stop')

def toggle_answer(question_id):
    for q in questions:
        if q["id"] == question_id:
            q["state"]["show_answer"] = not q["state"]["show_answer"]
            break

def add_new_question(question, answer):
    api_post("/add", {"question": question, "answer": answer})
    render_page()

def delete_question(path: str, id: int) -> None:
    """Send API delete and render the page for updates.
    
    Args:
        path: The path of the API ednpoint.
        id: The id of the question to delete.
    """
    if api_delete(path, id):
        render_page()

def update_question(path: str, id: int, question: str, answer: str, dialog) -> None:
    """Send API post and render the page for updates.
    
    Args:
        path: The path of the API ednpoint.
        id: The id of the question to modify.
        question: The update question of the question object.
        answer: The updated answer of the question object.
    """
    if api_put(path, id, data={"question": question, "answer": answer}):
        dialog.close()
        render_page()

def render_text_inputs():
    with ui.card().classes('w-64'):
        ui.label("Add a question").classes("text-lg font-bold")
        new_question_input = ui.input(label="New question").props("clearable").classes("w-full")
        new_answer_input = ui.input(label="New answer").props("clearable").classes("w-full")
        ui.button(text="Add question", on_click=lambda: add_new_question(
            question=new_question_input.value,
            answer=new_answer_input.value
        ))

def init_page():
    render_page()

def render_page():
    global questions
    questions = api_get("/questions")
    page_body_row.clear()
    page_body_col.clear()
    with page_body_row:
        with ui.element('div').style(
        'display: flex; overflow-x: auto; gap: 1rem; padding: 1rem;'
        ): 
            for question in questions:
                question["state"] = {"show_answer": False}
                render_question(question)
    with page_body_col:
        render_text_inputs()
    

init_page()
ui.run(port=8084, title="HCI Review Application")