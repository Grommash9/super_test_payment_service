from local_extension.db_methods.base import create_con, create_dict_con

async def get_all():
    con, cur = await create_dict_con()
    await cur.execute('select * from admin_panel_paymentstatus')
    status_data = await cur.fetchall()
    await con.ensure_closed()
    return status_data
