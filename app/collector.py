import json
import datetime
from . import api


def main(feed_id="0"):
    api.ensure_feed_exists(
        # Internal id for the feed, required
        feed_id,
        # Public name for the feed, required
        name="ip2-events",
        # Public title for the feed
        title="IP events",
        # Public short description of the feed/event
        summary_template=[
            "This is a short summary of the event. ",
            "We can use phrasing content like ",
            {"type": "em", "children": ["emphasis elements"]},
            " or ",
            {"type": "strong", "children": ["strong importance elements"]},
            " to make our point."
        ],
        # Public detailed description of the feed/event
        details_template=[
            {
                "type": "p",
                "props": {},
                "children": [
                    "This is the first paragraph of the detailed event description. ",
                    "We can use phrasing content here as well, or show a ",

                    "."
                ],
            },
            {
                "type": "x-if",
                "props": {
                    "path": ["event", "props", "timestamp"],
                },
                "children": [{
                    "type": "p",
                    "children": [
                        "If event.props.timestamp is 0, \"\", false, null, undefined " +
                        "or an empty array then this paragraph won't be shown. ",
                        "Here's event.props.timestamp as text: ",
                        {
                            "type": "x-text",
                            "props": {"path": ["event", "props", "timestamp"]}
                        }
                    ]
                }],
            }
        ]
    )

    for installation in api.list_installations():
        # Clean up uninstalled installations
        if installation["removed"]:
            api.delete_installation(installation["id"])
            continue

        installation_id = installation["id"]
        state = api.get_state(installation_id)

        event_props = {}
        if state.get("include_timestamps"):
            event_props["timestamp"] = datetime().isoformat()

        events = []
        for item in api.list_assets(installation_id):
            if item["type"] == "ip":
                events.append({
                    # Type can be "ip", "domain", "email" or "opaque".
                    "type": "ip",
                    # Value depends on the type, here it is an IP address, because
                    # item's type was "ip".
                    "value": item["value"],
                    # A Base64-encoded string used to separate different events
                    # with same type+value. Note that "" is a valid Base64 encoded string :)
                    "key": "",
                    # Freeform properties that can be used in the feed template to give
                    # more context about the event.
                    "props": event_props
                })

        # Send the events, ensuring that only the owner of this specific
        # installation can see them.
        api.send_events_for_installation(installation_id, feed_id, events)


if __name__ == "__main__":
    main()
