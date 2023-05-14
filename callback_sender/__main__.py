import datetime
import time
from local_extension import db_methods
import requests

while True:
    callbacks_to_send = db_methods.admin_panel_paymentcallbacksendlog.get_callbacks_to_send()

    for callback in callbacks_to_send:
        try:
            resp = requests.post(callback['callback_url'], json=callback)
            status_code = resp.status_code
            response_text = resp.text
        except Exception as e:
            response_text = str(e)
            status_code = 0
        db_methods.admin_panel_paymentcallbacksendlog.update_as_sent(
            callback['call_id'], status_code, response_text[:1500], datetime.datetime.now())
        time.sleep(1)
    time.sleep(1)
