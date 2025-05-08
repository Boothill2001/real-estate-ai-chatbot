class MCPManager:
    def __init__(self):
        self.sessions = {}

    def save_context(self, session_id, query, plan, results):
        self.sessions[session_id] = {
            "last_query": query,
            "last_plan": plan,
            "last_results": results,
        }

    def load_context(self, session_id):
        return self.sessions.get(session_id, None)

    def clear_context(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

import sqlite3
class MCPManagerSQL:
    def __init__(self, db_path="mcp_sessions.db"):
        self.conn = sqlite3.connect(db_path)
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
        ''', (session_id, query, str(plan), str(results)))
        self.conn.commit()

    def load_context(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT last_query, last_plan, last_results FROM sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        if row:
            return {
                "last_query": row[0],
                "last_plan": eval(row[1]),
                "last_results": eval(row[2])
            }
        return None

    def clear_context(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        self.conn.commit()
