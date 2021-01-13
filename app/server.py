import re
from flask import Flask, request, abort, jsonify
from . import api

def get_bearer_token():
    auth = request.headers.get("Authorization", "")
    match = re.match(r"^Bearer\s+([a-z0-9-._~+/]+=*)$", auth, re.I)
    return match.group(1) if match else None


def do_update(installation_state, client_state):
    installation_state["name"] = client_state["name"]
    installation_state["checked"] = client_state["checked"]
    return installation_state


def create_app():
    app = Flask(__name__)

    @app.route("/app/ui", methods=["POST"])
    def ui():
        # Get the bearer token and check its validity using the Badrap API.
        token = get_bearer_token()
        if not token:
            abort(403)
        token_info = api.get_token_info(token)
        if not token_info:
            abort(403)
        installation_id = token_info["installationId"]

        payload = request.json.get("payload", {})
        action = payload.get("action")
        client_state = payload.get("clientState", {})
        if action == "update":
            installation_state = api.update_state(installation_id, do_update, client_state)
        else:
            installation_state = api.get_state(installation_id)

        return jsonify([
            {
                # Box is a basic layout element that accepts (almost) any TailwindCSS class.
                "type": "Box",
                "props": {
                    "class": "w-full mb-2"
                },
                "children": [
                    "Name",
                    {
                        "type": "TextField",
                        "props": {
                            # The field value is sent in clientState.name
                            # when the submit button is clicked.
                            "name": "name",
                            # The text field needs to have a value for
                            # the submit button to work.
                            "required": True,
                            # The initial value of the text field.
                            "value": installation_state.get("name", "")
                        }
                    }
                ]
            },
            {
                "type": "Box",
                "props": {
                    "class": "w-full mb-2"
                },
                "children": [
                    "Checked",
                    {
                        "type": "Checkbox",
                        "props": {
                            "name": "checked",
                            "checked": installation_state.get("checked", False)
                        }
                    }
                ]
            },
            {

                "type": "Button",
                "props": {
                    # Automatically act as a submit button for the enclosing form
                    # (the whole UI is also implicitly a form).
                    # This basically means that the button gets enabled/disabled
                    # when requires inputs are filled etc.
                    "submit": True,
                    # Clicking the button sends the given action (can be any JSON value)
                    # plus the inputs' state back to this function.
                    "action": "update",
                    # Variant can be "default", "primary" and "danger".
                    "variant": "primary",
                },
                "children": [
                    "Update state"
                ]
            }
        ])


    return app
