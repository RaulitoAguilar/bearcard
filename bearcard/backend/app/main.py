import csv, io, sqlite3, time
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from .ml import rank_cards

DB = "/data/bearcard.db"
app = FastAPI()


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


with db() as con:
    con.executescript("""
    CREATE TABLE IF NOT EXISTS cards(
      id INTEGER PRIMARY KEY, topic TEXT, subtopic TEXT, question TEXT, answer TEXT);
    CREATE TABLE IF NOT EXISTS answers(
      id INTEGER PRIMARY KEY, card_id INTEGER, correct INTEGER, time_ms INTEGER, ts REAL);
    """)


class Card(BaseModel):
    topic: str
    subtopic: str = ""
    question: str
    answer: str


class Answer(BaseModel):
    card_id: int
    correct: bool
    time_ms: int


@app.get("/api/topics")
def topics():
    with db() as con:
        return [r[0] for r in con.execute("SELECT DISTINCT topic FROM cards ORDER BY topic")]


@app.post("/api/cards")
def add_card(c: Card):
    with db() as con:
        con.execute("INSERT INTO cards(topic,subtopic,question,answer) VALUES(?,?,?,?)",
                    (c.topic, c.subtopic, c.question, c.answer))
    return {"ok": True}


@app.post("/api/import")
async def import_csv(file: UploadFile):
    text = (await file.read()).decode("utf-8-sig")
    rows = [r for r in csv.reader(io.StringIO(text)) if len(r) >= 4]
    with db() as con:
        con.executemany("INSERT INTO cards(topic,subtopic,question,answer) VALUES(?,?,?,?)",
                        [r[:4] for r in rows])
    return {"imported": len(rows)}


@app.get("/api/session")
def session(topic: str, limit: int = 10):
    with db() as con:
        cards = [dict(r) for r in con.execute("SELECT * FROM cards WHERE topic=?", (topic,))]
        answers = [dict(r) for r in con.execute("SELECT * FROM answers ORDER BY ts")]
    return rank_cards(cards, answers)[:limit]


@app.post("/api/answer")
def answer(a: Answer):
    with db() as con:
        con.execute("INSERT INTO answers(card_id,correct,time_ms,ts) VALUES(?,?,?,?)",
                    (a.card_id, int(a.correct), a.time_ms, time.time()))
    return {"ok": True}


@app.get("/api/history")
def history():
    with db() as con:
        rows = con.execute("""SELECT c.topic, c.question, a.correct, a.time_ms
                              FROM answers a JOIN cards c ON c.id=a.card_id
                              ORDER BY a.ts DESC LIMIT 50""")
        return [dict(r) for r in rows]
