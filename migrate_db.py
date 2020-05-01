# from peewee import CharField
from playhouse.migrate import migrate, CharField, SqliteDatabase, SqliteMigrator
# from playhouse.migrate import *

my_db = SqliteDatabase('my_app.db')
migrates = SqliteMigrator(my_db)
result_gsc = CharField(null=True)
result_sofa = CharField(null=True)
with my_db.atomic():
    migrate(
        migrates.add_column('requestuser', 'result_sofa', result_sofa),
        migrates.add_column('requestuser', 'result_gsc', result_gsc),
            )
