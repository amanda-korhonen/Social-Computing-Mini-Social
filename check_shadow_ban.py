"""
Generated with Claude sonnet 5.5.
prompt: how to test if the shadow ban is over now? for a certain user?
Shows whether a user's shadow ban is running or over.
Run from the project folder:   python check_shadow_ban.py <username>
"""
import sqlite3
import sys
from datetime import datetime, timezone

DATABASE = "database.sqlite"

if len(sys.argv) != 2:
    sys.exit("Usage: python check_shadow_ban.py <username>")

conn = sqlite3.connect(DATABASE)
row = conn.execute("SELECT shadow_banned_until, shadow_ban_count FROM users WHERE username = ?",
                   (sys.argv[1],)).fetchone()
if not row:
    sys.exit(f"No such user: {sys.argv[1]}")

until, count = row
now = datetime.now(timezone.utc).replace(tzinfo=None)
print(f"Shadow bans so far: {count or 0}")

if not until:
    print("Not banned (has never been shadow banned).")
else:
    ends = datetime.strptime(until, "%Y-%m-%d %H:%M:%S")
    if ends > now:
        left = ends - now
        hours, rest = divmod(int(left.total_seconds()), 3600)
        print(f"BAN IS RUNNING until {until} UTC ({hours}h {rest // 60}m left).")
    else:
        print(f"Ban is over (ended {until} UTC).")
conn.close()