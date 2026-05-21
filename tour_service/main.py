from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Tour Service - Павло Голубчак")

# Персоналізація (твій номер у групі)
STUDENT_N = 18   # ← Зміни на свій номер, якщо інший

class Tour(BaseModel):
    id: int
    name: str
    description: str
    price: float
    duration_days: int
    available: bool = True

# Імітація бази даних
TOURS = {
    STUDENT_N * 100 + 1: Tour(id=STUDENT_N*100+1, name="Карпати Тур", description="Гори, природа, чани", price=4500, duration_days=5, available=True),
    STUDENT_N * 100 + 2: Tour(id=STUDENT_N*100+2, name="Море - Одеса", description="Відпочинок на Чорному морі", price=7200, duration_days=7, available=True),
    STUDENT_N * 100 + 3: Tour(id=STUDENT_N*100+3, name="Європа: Польща+Словаччина", description="Автобусний тур", price=8900, duration_days=8, available=False),
}

@app.get("/tours")
def get_all_tours():
    return {"tours": list(TOURS.values()), "student_id": STUDENT_N}

@app.get("/tours/{tour_id}")
def get_tour(tour_id: int):
    if tour_id not in TOURS:
        raise HTTPException(status_code=404, detail="Tour not found")
    return {"data": TOURS[tour_id], "student_id": STUDENT_N}