from fastapi_cache import caches
from fastapi_cache.backends.memory import CACHE_KEY

conventions = {
    'all_column_name': lambda constraint, table: '_'.join([
       column.name for column in constraint.columns.values()
    ]),
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def redis_cache():
    return caches.get(CACHE_KEY)

