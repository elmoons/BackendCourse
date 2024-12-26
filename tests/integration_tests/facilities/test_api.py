

async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    print(response)
    assert response.status_code == 200


async def test_add_facilities(ac):
    response = await ac.post("/facilities", json={"title": "fridge"})
    assert response.status_code == 200
