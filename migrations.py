# migrations.py is for building your database

async def m001_initial(db):
   await db.execute(
       """
       CREATE TABLE reviews.surveys (
          "user" TEXT,
           id TEXT PRIMARY KEY,
           meta TEXT DEFAULT '{}'
       );
   """)