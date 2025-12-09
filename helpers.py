import requests
import json
import time


def retrieve_phone_code(driver):
    """
    Retrieves the confirmation code from the browser performance logs.
    Includes a sleep timer to poll for the code effectively.
    """
    code = None
    for i in range(10):
        try:
            # Get performance logs
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")]

            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                message_body = message_data.get("message", {})

                # Check if this log entry is a network response
                if message_body.get("method") == "Network.responseReceived":
                    url = message_body.get("params", {}).get("response", {}).get("url", "")

                    # We only care about the phone auth response
                    if "/api/v1/auth/phone" in url:
                        request_id = message_body["params"]["requestId"]
                        body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        code = body['body']['code']
                        # Once we find the code, return it immediately!
                        return code
        except Exception:
            pass

        # CRITICAL FIX: Wait 1 second before checking again
        # Without this, the loop finishes instantly before the SMS arrives.
        time.sleep(1)

    return code


def is_url_reachable(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False