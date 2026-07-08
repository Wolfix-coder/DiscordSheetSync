ALLOWED_TABLES = {
    'user_data': ['STEAM_ID'],

}

def validate_table_column(table: str, column: str):
        if table not in ALLOWED_TABLES:
            raise ValueError(f"❌ Таблиця '{table}' не дозволена")
        
        if column not in ALLOWED_TABLES[table]:
            raise ValueError(f"❌ Колонка '{column}' не існує в таблиці '{table}'")