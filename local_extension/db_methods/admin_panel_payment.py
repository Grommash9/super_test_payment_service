from local_extension.db_methods.base import create_con, create_dict_con


async def create_new(uuid, amount, cur_code, callback_url: str = None):
    con, cur = await create_con()
    await cur.execute('insert into admin_panel_payment (uuid, amount, currency, callback_url, status_id) '
                      'VALUES (%s,%s,%s,%s,(select record_id from admin_panel_paymentstatus where `code` = %s))',
                      (uuid, amount, cur_code, callback_url, 'created'))
    await con.commit()
    await con.ensure_closed()


async def get(uuid):
    con, cur = await create_dict_con()
    await cur.execute('select uuid, amount, currency, callback_url, status_id '
                      'from admin_panel_payment where uuid = %s ', (uuid,))
    payment_info = await cur.fetchone()
    await con.ensure_closed()
    if payment_info is None:
        return None
    return payment_info
