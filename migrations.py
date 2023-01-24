# migrations.py is for building your database

async def m001_initial(db):
   await db.execute(
       """
       CREATE TABLE reviews.surveys (
           id TEXT PRIMARY KEY,
           wallet TEXT NOT NULL,
           meta TEXT DEFAULT '{}'
       );
   """)

   
