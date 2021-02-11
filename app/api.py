import os
import json
import urllib
import requests

API_URL = os.environ["API_URL"]
API_TOKEN = os.environ["API_TOKEN"]


def api_request(method, path, raise_for_status=True, headers=None, timeout=15, **kwargs):
    url = urllib.parse.urljoin(API_URL + "/", "./" + path)
    headers = dict(headers) if headers else {}
    headers.setdefault("Authorization", f"Bearer {API_TOKEN}")
    response = requests.request(
        method,
        url,
        headers=headers,
        timeout=timeout,
        **kwargs
    )
    if raise_for_status:
        response.raise_for_status()
    return response


def list_installations():
    return api_request("GET", "/app/installations").json()


def delete_installation(installation_id):
    return api_request("DELETE", f"/app/installations/{installation_id}")


def get_token_info(token):
    res = api_request(
        "POST",
        "/app/token",
        json={"token": token},
        raise_for_status=False
    )
    if res.status_code == 404:
        return None
    res.raise_for_status()
    return res.json()


def get_state(installation_id):
    res = api_request("GET", f"/app/installations/{installation_id}")
    json = res.json()
    return json["state"]


def update_state(installation_id, updater, *args, **kwargs):
    while True:
        res = api_request("GET", f"/app/installations/{installation_id}")
        etag = res.headers.get("etag", "*")
        old_state = res.json()["state"]

        new_state = updater(old_state, *args, **kwargs)
        if new_state is None:
            return old_state

        res = api_request(
            "PATCH",
            f"/app/installations/{installation_id}",
            headers={"If-Match": etag},
            json={"state": new_state},
            raise_for_status=False
        )
        if res.status_code == 412:
            continue
        res.raise_for_status()
        return new_state


def list_assets(installation_id):
    res = api_request(
        "GET",
        f"/app/installations/{installation_id}/owner/assets"
    )
    return res.json()


def ensure_feed_exists(feed_id, name, title=None, summary_template=None, details_template=None):
    res = api_request(
        "PUT",
        f"/app/feeds/{feed_id}",
        json={
            "name": name,
            "title": title,
            "summaryTemplate": summary_template,
            "detailsTemplate": details_template
        }
    )


def send_events_for_installation(installation_id, feed_id, events):
    event_lines = "\n".join(json.dumps(e) for e in events)
    res = api_request(
        "POST",
        f"/app/installations/{installation_id}/feeds/{feed_id}/events",
        data=event_lines
    )
