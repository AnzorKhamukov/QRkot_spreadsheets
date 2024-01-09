from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.constants import FORMAT_DATE, SPREADSHEET_BODY, TABLE_HEAD


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT_DATE)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEET_BODY
    spreadsheet_body['properties']['title'] = f'Отчет от {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheet_Id']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT_DATE)
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = TABLE_HEAD
    table_head[0] = ['Отчет от', now_date_time]

    table_values = [
        *table_head,
        *[list(map(str, project.values())) for project in projects],
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    num_rows = len(table_values)
    num_columns = len(table_values[0]) if table_values else 0

    range_start = 'A1'
    if num_columns > 0:
        range_end = chr(65 + num_columns - 1) + str(num_rows)
        range_to_update = f'{range_start}:{range_end}'
    else:
        range_to_update = range_start

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheet_Id=spreadsheet_id,
            range=range_to_update,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
