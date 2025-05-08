# agents/utils/mcp_manager_sql.py

import sqlite3
import json

class MCPManagerSQL:
    def __init__(self, db_path="mcp_sessions.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                last_query TEXT,
                last_plan TEXT,
                last_results TEXT
            )
        ''')
        self.conn.commit()

    def save_context(self, session_id, query, plan, results):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO sessions (session_id, last_query, last_plan, last_results)
            VALUES (?, ?, ?, ?)
        ''', (session_id, query, json.dumps(plan), json.dumps(results)))
        self.conn.commit()

    def load_context(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT last_query, last_plan, last_results FROM sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        if row:
            return {
                "last_query": row[0],
                "last_plan": json.loads(row[1]),
                "last_results": json.loads(row[2])
            }
        return None

    def clear_context(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        self.conn.commit()
