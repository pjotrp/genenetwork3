"""module contains all db related stuff"""
import contextlib
from typing import Any, Iterator, Protocol, Tuple
from urllib.parse import urlparse
import MySQLdb as mdb
import xapian


def parse_db_url(sql_uri: str) -> Tuple:
    """function to parse SQL_URI env variable note:there\
    is a default value for SQL_URI so a tuple result is\
    always expected"""
    parsed_db = urlparse(sql_uri)
    return (
        parsed_db.hostname, parsed_db.username, parsed_db.password,
        parsed_db.path[1:], parsed_db.port)


# pylint: disable=missing-class-docstring, missing-function-docstring, too-few-public-methods
class Connection(Protocol):
    """Type Annotation for MySQLdb's connection object"""
    def cursor(self, *args) -> Any:
        """A cursor in which queries may be performed"""
        ...


@contextlib.contextmanager
def database_connection(sql_uri) -> Iterator[Connection]:
    """Connect to MySQL database."""
    host, user, passwd, db_name, port = parse_db_url(sql_uri)
    connection = mdb.connect(db=db_name,
                             user=user,
                             passwd=passwd or '',
                             host=host,
                             port=port or 3306)
    try:
        yield connection
    finally:
        connection.close()


@contextlib.contextmanager
def xapian_database(path):
    """Open xapian database read-only."""
    # pylint: disable-next=invalid-name
    db = xapian.Database(path)
    try:
        yield db
    finally:
        db.close()
