import aiosqlite
from typing import Any, Optional, Dict

from src.utils.validators import validate_table_column
from config import Config

class DBCreator:
    @staticmethod
    async def create_tables() -> bool:
        try:
            async with aiosqlite.connect(Config.DATABASE_PATH) as db:
                await db.execute(
                    """CREATE TABLE IF NOT EXISTS user_data (
                        STEAM_ID INTEGER PRIMARY KEY,
                        USERNAME TEXT)"""
                )
                await db.commit()
                return True
        except aiosqlite.Error as e:
            print(f" ERROR    -- -- Error create table user_data: {e}")
            return False
        except Exception as e:
            print(f" ERROR    -- -- Помилка під час створення бази данних: {e}")
            return False

class DBService:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH

    async def _get_db_connection(self):
        try:
            db = await aiosqlite.connect(self.db_path)
            db.row_factory = aiosqlite.Row # Для повернення інформації у вигляді (id = '1234', name = 'John', ...)
            return db
        except Exception as e:
            print(f" ERROR    -- -- Помилка підключення до БД: {e}")
            raise
    
    async def get_by_id(self, table: str, column: str, id_value: Any) -> Optional[Dict]:
        """
        Отримання одного запису по ID

        Args:
            table: str - назва таблиці (наприклад 'payments')
            column: str - назва поля ID (наприклад 'ID_worker')
            id_value: Any - значення ID (може бути str "001234" або int 123)
        
        Return:
            Optional[Dict] - словник зі всіма знайденими значеннями, або None якщо не знайдено
        """
        db = None

        try:
           db = await self._get_db_connection()
           validate_table_column(table, column) # Валідація table and column
           async with db.execute(f"SELECT * FROM {table} WHERE {column} = ?", (id_value,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
        except aiosqlite.Error as e:
            print(f" ERROR    -- -- Помилка отримання данних з бд: ")
            raise
        except ValueError as e:
            print(f" ERROR    -- -- Помилка валідації: ")
            raise
        finally:
            if db:
                await db.close()

    async def create_user(self, steam_id: str, username: str):
        """
        Запис рядку в базу данних

        Args:
            steam_id: str -- id гравця
            username: str -- username гравця
        """
        try:
            db = await self._get_db_connection()

            await db.execute(
                "INSERT INTO user_data (STEAM_ID, USERNAME) VALUES (?, ?)",
                (steam_id, username))
            await db.commit()

        except aiosqlite.Error as e:
            print(f" ERROR    -- -- Помилка запису данних з бд: ")
            raise
        finally:
            if db:
                await db.close()
