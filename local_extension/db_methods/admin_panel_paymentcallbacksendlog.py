from local_extension.db_methods.base import sync_create_con, sync_dict_con



def get_callbacks_to_send():
    con, cur = sync_dict_con()
    cur.execute('select payment.uuid, payment.status_id, payment.amount, payment.currency, '
                'payment.callback_url, calllog.record_id as "call_id" '
                'from admin_panel_paymentcallbacksendlog calllog '
                'join admin_panel_payment payment on calllog.payment_associated_id = payment.record_id '
                'where calllog.sent_result is Null ')
    call_back_data = cur.fetchall()
    con.close()
    return call_back_data


def update_as_sent(call_event_id, result, status_code, time):
    con, cur = sync_dict_con()
    cur.execute('update admin_panel_paymentcallbacksendlog '
                'set sent_date = %s, '
                'send_status = %s, '
                'sent_result = %s where record_id = %s ',
                (time, result, status_code, call_event_id))
    con.commit()
    con.close()
