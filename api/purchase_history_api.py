
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from faker import Faker

import random
import datetime

app = FastAPI()
fake = Faker()


stores = ["Big Bazaar", "DMart", "Reliance Fresh", "Spencer's", "More"]

class MobileList(BaseModel):
    mobiles: List[str]

def generate_purchase(mobile: str):
    # Randomly introduce missing or malformed values
    if random.random() < 0.1:
        date = None
    elif random.random() < 0.1:
        date = fake.date(pattern="%d-%m-%Y")  # Non-standard format
    else:
        date = fake.date(pattern="%Y-%m-%d")

    amount = round(random.uniform(100, 10000), 2) if random.random() > 0.05 else None
    store = random.choice(stores) if random.random() > 0.05 else None

    return {
        "mobile": mobile,
        "date": date,
        "amount": amount,
        "store": store
    }

@app.post("/purchase-history")
def get_purchase_history(request: MobileList):
    purchases = []
    for mobile in request.mobiles:
        purchases.extend([generate_purchase(mobile) for _ in range(random.randint(3, 10))])
    # Introduce duplicates
    if random.random() < 0.2:
        purchases += random.choices(purchases, k=2)

    #return JSONResponse(content={"purchases": purchases})
    return {"purchases": purchases}
