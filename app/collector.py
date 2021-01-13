import json
from . import api


def main():
    for installation in api.list_installations():
        # Clean up uninstalled installations
        if installation["removed"]:
            api.delete_installation(installation["id"])
            continue

        installation_id = installation["id"]
        state = api.get_state(installation_id)

        print("Installation {}".format(installation_id))
        print("  State: {}", json.dumps(state))
        print("  Assets:")
        for item in api.list_assets(installation_id):
            print("    {}".format(json.dumps(item)))


if __name__ == "__main__":
    main()
