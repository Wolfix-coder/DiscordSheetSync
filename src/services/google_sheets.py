from gspread import Client, Worksheet, Spreadsheet, service_account
from gspread.worksheet import ValidationConditionType

from config import Config

class GoogleSheetsService:
    def client_init_json(self) -> Client:
        """Створення клієнта для роботи з Google Sheets"""
        return service_account(filename=Config.JSON_CONFIG_PATH)
    
    def get_table_by_url(self, client: Client, table_url) -> Worksheet:
        """Отримує таблиці із Google Sheets за посиланням."""
        return client.open_by_url(table_url).sheet1

    def get_table_by_id(self, client: Client, table_id) -> Worksheet:
        """Отримує таблиці із Google Sheets за ID таблиці."""
        return client.open_by_key(table_id).sheet1
    
    def append_row(self, worksheet: Worksheet, data: list):
        """Додає рядок даних у кінець таблиці."""
        worksheet.append_row(data)

    def setup_status_dropdown(self, worksheet: Worksheet, column: int = 5, 
                                start_row: int = 2, end_row: int = 1000):
        sheet_id = worksheet.id
        col_letter = chr(64 + column)
        cell_range_a1 = f"{col_letter}{start_row}:{col_letter}{end_row}"

        statuses = ["Принял", "Отклонил", "Ещё висит", "Удалил из друзей"]

        worksheet.add_validation(
            cell_range_a1,
            ValidationConditionType.one_of_list,
            statuses,
            showCustomUi=True
        )

        # 2. Кольори для кожного варіанту
        cell_range = {
            "sheetId": sheet_id,
            "startRowIndex": start_row - 1,
            "endRowIndex": end_row,
            "startColumnIndex": column - 1,
            "endColumnIndex": column,
        }

        colors = {
            "Принял": {"red": 0.2, "green": 0.66, "blue": 0.33},
            "Отклонил": {"red": 0.8, "green": 0.2, "blue": 0.2},
            "Ещё висит": {"red": 0.4, "green": 0.4, "blue": 0.4},
            "Удалил из друзей": {"red": 0.4, "green": 0.2, "blue": 0.6},
        }

        requests = []
        for text, color in colors.items():
            requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [cell_range],
                        "booleanRule": {
                            "condition": {
                                "type": "TEXT_EQ",
                                "values": [{"userEnteredValue": text}]
                            },
                            "format": {
                                "backgroundColor": color,
                                "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}}
                            }
                        }
                    },
                    "index": 0
                }
            })

        worksheet.spreadsheet.batch_update({"requests": requests})