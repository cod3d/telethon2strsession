import ipaddress
import struct
import sys
from pathlib import Path
from typing import Iterator

from telethon.sessions.string import StringSession, CURRENT_VERSION, _STRUCT_PREFORMAT
from peewee import SqliteDatabase

from database import Session as SessionTable


def get_sessions(db_path: Path) -> Iterator[str]:
    """
    Iterates sessions from the database
    :param db_path: the database path
    :return: Iterator[StringSession]
    """
    print(f'looking for sessions in {db_path}...')

    class NSessionTable(SessionTable):
        class Meta:
            database = SqliteDatabase(db_path)
            table_name = 'sessions'

    if not NSessionTable.table_exists():
        print(f'The database {db_path} does not contain `sessions` table')
        return

    record: NSessionTable
    for record in NSessionTable.select():
        if record.server_address is None or record.port is None or record.auth_key is None:
            print(f'[{record.dc_id}] record is invalid. skip.')
            continue
        print(f'[{record.dc_id}] session found')
        r_ip = ipaddress.ip_address(record.server_address).packed
        yield CURRENT_VERSION + StringSession.encode(struct.pack(
            _STRUCT_PREFORMAT.format(len(r_ip)),
            record.dc_id,
            r_ip,
            record.port,
            record.auth_key
        ))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:\n\tpython main.py "D:\\telegram\\session.session"')
    else:
        db_path_ = Path(sys.argv[1])
        if not db_path_.exists():
            print(f'The database path {db_path_} does not exist')
        else:
            sessions = list(get_sessions(db_path_))
            print(f'Found {len(sessions)} sessions')

            if len(sessions) > 0:
                print('\n=== SESSIONS ===\n')
                print('\n\t'.join(sessions))
