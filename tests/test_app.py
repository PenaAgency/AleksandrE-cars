import pytest

MOCK_NEW_DEALER_1 = {
    "dealer_name": "dealer_1",
    "address": "address_1",
    "phone": 10000000001,
}

MOCK_NEW_DEALER_2 = {
    "dealer_name": "dealer_2",
    "address": "address_1",
    "phone": 10000000002,
}

MOCK_NEW_DEALER_3 = {
    "dealer_name": "dealer_3",
    "address": "address_2",
    "phone": 10000000001,
}

MOCK_NEW_CAR_1 = {
    "model": "model_1",
    "year": 2001,
    "color": "color_1",
    "mileage": 1,
    "price": 1,
}

MOCK_NEW_CAR_2 = {
    "model": "model_1",
    "year": 2002,
    "color": "color_1",
    "mileage": 1,
    "price": 2,
}

MOCK_NEW_CAR_3 = {
    "model": "model_2",
    "year": 2002,
    "color": "color_1",
    "mileage": 2,
    "price": 2,
}


class TestCreateDealer:
    @pytest.mark.parametrize(
        ("request_body", "dealer"),
        [
            (
                {"dealer_name": "name"},
                {"address": None, "dealer_name": "name", "phone": None},
            ),
            (
                {"dealer_name": "name", "address": "address"},
                {"address": "address", "dealer_name": "name", "phone": None},
            ),
            (
                {
                    "dealer_name": "name",
                    "address": "address",
                    "phone": 10000000001,
                },
                {
                    "address": "address",
                    "dealer_name": "name",
                    "phone": 10000000001,
                },
            ),
        ],
    )
    def test_create_dealer_with_different_parameters(
        self, testing_app, request_body, dealer, create_dealer_search_response
    ):
        response = testing_app.post(url="/dealer", json=request_body)
        assert response.status_code == 201
        assert response.json() == {"detail": "created"}
        response = testing_app.post(url="/dealer/search", json={})
        dealer_id = response.json()[0]["id"]
        assert response.json() == [dealer | {"id": dealer_id}]

    def test_create_dealer_when_dealer_name_is_not_specified(
        self, testing_app
    ):
        response = testing_app.post(url="/dealer", json={})
        assert response.status_code == 422

    def test_create_dealers_with_the_different_dearer_names(
        self, testing_app, create_dealer_search_response
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        response = testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        assert response.status_code == 201
        assert response.json() == {"detail": "created"}
        all_dealers = testing_app.post(url="/dealer/search", json={})
        assert all_dealers.json() == create_dealer_search_response(
            MOCK_NEW_DEALER_1, MOCK_NEW_DEALER_2
        )

    def test_create_dealers_with_the_same_dealer_name(
        self, testing_app, create_dealer_search_response
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        response = testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        assert response.status_code == 409
        all_dealers = testing_app.post(url="/dealer/search", json={})
        assert all_dealers.json() == create_dealer_search_response(
            MOCK_NEW_DEALER_1
        )


WRONG_ID = 11111111
WRONG_PHONE = 12000000000


class TestGetDealer:
    def test_get_dealers_when_database_is_empty(self, testing_app):
        response = testing_app.post(url="/dealer/search", json={})
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize(
        ("request_body", "result"),
        [
            ({}, [MOCK_NEW_DEALER_1, MOCK_NEW_DEALER_2, MOCK_NEW_DEALER_3]),
            ({"dealer_name": "dealer_1"}, [MOCK_NEW_DEALER_1]),
            ({"address": "address_1"}, [MOCK_NEW_DEALER_1, MOCK_NEW_DEALER_2]),
            ({"phone": 10000000001}, [MOCK_NEW_DEALER_1, MOCK_NEW_DEALER_3]),
            (
                {
                    "dealer_name": "dealer_1",
                    "address": "address_1",
                    "phone": 10000000001,
                },
                [MOCK_NEW_DEALER_1],
            ),
            ({"dealer_name": "wrong_name"}, []),
            ({"dealer_name": "dealer_1", "phone": WRONG_PHONE}, []),
            ({"id": WRONG_ID}, []),
        ],
    )
    def test_get_dealers(
        self, testing_app, request_body, result, create_dealer_search_response
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_3)
        all_dealers = testing_app.post(url="/dealer/search", json=request_body)
        assert all_dealers.status_code == 200
        assert all_dealers.json() == create_dealer_search_response(*result)

    def test_get_dealer_by_id(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        all_dealers = testing_app.post(url="/dealer/search", json={})
        dealer_1_id = all_dealers.json()[0]["id"]
        response = testing_app.post(
            url="/dealer/search", json={"id": dealer_1_id}
        )
        assert response.status_code == 200
        assert response.json() == [MOCK_NEW_DEALER_1 | {"id": dealer_1_id}]


class TestChangeDealer:
    @pytest.mark.parametrize(
        ("request_body", "result"),
        [
            (
                {"dealer_name": "new_name"},
                {
                    "address": "address_1",
                    "dealer_name": "new_name",
                    "phone": 10000000001,
                },
            ),
            (
                {"address": "new_address"},
                {
                    "address": "new_address",
                    "dealer_name": "dealer_1",
                    "phone": 10000000001,
                },
            ),
            (
                {"phone": 18000000001},
                {
                    "address": "address_1",
                    "dealer_name": "dealer_1",
                    "phone": 18000000001,
                },
            ),
            (
                {
                    "dealer_name": "new_name",
                    "address": "new_address",
                    "phone": 18000000001,
                },
                {
                    "address": "new_address",
                    "dealer_name": "new_name",
                    "phone": 18000000001,
                },
            ),
            (
                {},
                {
                    "address": "address_1",
                    "dealer_name": "dealer_1",
                    "phone": 10000000001,
                },
            ),
        ],
    )
    def test_change_dealer(self, testing_app, request_body, result):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        dealer = testing_app.post(url="/dealer/search", json={})
        dealer_id = dealer.json()[0]["id"]
        response = testing_app.put(
            url=f"/dealer/{dealer_id}", json=request_body
        )
        assert response.status_code == 200
        assert response.json() == {"detail": "changed"}
        dealer = testing_app.post(url="/dealer/search", json={})
        assert dealer.json() == [result | {"id": dealer_id}]

    def test_change_dealer_when_dealer_does_not_exist(self, testing_app):
        wrong_dealer_id = 1
        response = testing_app.put(
            url=f"/dealer/{wrong_dealer_id}", json={"dealer_name": "some_name"}
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "dealer with this ID doesn't exist"
        }

    def test_change_dealer_name_when_dealer_with_this_name_already_exist(
        self, testing_app
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        all_dealers = testing_app.post(url="/dealer/search", json={})
        dealer_1_id = all_dealers.json()[0]["id"]
        dealer_2_name = all_dealers.json()[1]["dealer_name"]
        response = testing_app.put(
            url=f"/dealer/{dealer_1_id}", json={"dealer_name": dealer_2_name}
        )
        assert response.status_code == 409


class TestDeleteDealer:
    def test_delete_dealer(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        all_dealers = testing_app.post(url="/dealer/search", json={})
        dealer_id = all_dealers.json()[0]["id"]
        response = testing_app.delete(url=f"/dealer/{dealer_id}")
        assert response.status_code == 200
        assert response.json() == {"detail": "deleted"}

    def test_delete_dealer_when_dealer_does_not_exist(self, testing_app):
        wrong_dealer_id = 1
        response = testing_app.delete(url=f"/dealer/{wrong_dealer_id}")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "dealer with this ID doesn't exist"
        }

    def test_delete_the_same_dealer_for_the_second_time(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        dealer = testing_app.post(url="/dealer/search", json={})
        dealer_id = dealer.json()[0]["id"]
        testing_app.delete(url=f"/dealer/{dealer_id}")
        response = testing_app.delete(url=f"/dealer/{dealer_id}")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "dealer with this ID doesn't exist"
        }

    def test_delete_dealer_when_dealer_has_cars(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        dealer = testing_app.post(url="/dealer/search", json={})
        dealer_id = dealer.json()[0]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )
        response = testing_app.delete(url=f"/dealer/{dealer_id}")
        assert response.status_code == 409


class TestCreateCar:
    @pytest.mark.parametrize(
        ("request_body", "car"),
        [
            (
                {
                    "model": "model",
                },
                {
                    "model": "model",
                    "year": None,
                    "color": None,
                    "mileage": None,
                    "price": None,
                },
            ),
            (
                {
                    "model": "model",
                    "year": 2010,
                },
                {
                    "model": "model",
                    "year": 2010,
                    "color": None,
                    "mileage": None,
                    "price": None,
                },
            ),
            (
                {
                    "model": "model",
                    "color": "color",
                },
                {
                    "model": "model",
                    "year": None,
                    "color": "color",
                    "mileage": None,
                    "price": None,
                },
            ),
            (
                {
                    "model": "model",
                    "mileage": 1,
                },
                {
                    "model": "model",
                    "year": None,
                    "color": None,
                    "mileage": 1,
                    "price": None,
                },
            ),
            (
                {
                    "model": "model",
                    "price": 1,
                },
                {
                    "model": "model",
                    "year": None,
                    "color": None,
                    "mileage": None,
                    "price": 1,
                },
            ),
            (
                {
                    "model": "model",
                    "year": 2010,
                    "color": "color",
                    "mileage": 1,
                    "price": 1,
                },
                {
                    "model": "model",
                    "year": 2010,
                    "color": "color",
                    "mileage": 1,
                    "price": 1,
                },
            ),
        ],
    )
    def test_create_car_with_different_parameters(
        self, testing_app, request_body, car
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        response = testing_app.post(url="/dealer/search", json={})
        dealer_id = response.json()[0]["id"]
        response = testing_app.post(
            url="/car", json=request_body | {"dealer_id": dealer_id}
        )
        assert response.status_code == 201
        assert response.json() == {"detail": "created"}
        response = testing_app.post(url="/car/search", json={})
        car_id = response.json()[0]["id"]
        assert response.json() == [
            car | {"dealer_id": dealer_id, "id": car_id}
        ]

    def test_create_car_when_dealer_does_not_exist(self, testing_app):
        wrong_dealer_id = 1
        response = testing_app.post(
            url="/car", json={"model": "model", "dealer_id": wrong_dealer_id}
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "dealer with this ID doesn't exist"
        }

    def test_create_car_when_car_model_does_not_specified(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        response = testing_app.post(url="/dealer/search", json={})
        dealer_id = response.json()[0]["id"]
        response = testing_app.post(url="/car", json={"dealer_id": dealer_id})
        assert response.status_code == 422


WRONG_YEAR = 1980
WRONG_MILEAGE = 111111
WRONG_PRICE = 111111
WRONG_DEALER_ID = 11111111
WRONG_CAR_ID = 11111111


class TestGetCar:
    def test_get_cars_when_database_is_empty(self, testing_app):
        response = testing_app.post(url="/car/search", json={})
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize(
        ("request_body", "result"),
        [
            ({}, [MOCK_NEW_CAR_1, MOCK_NEW_CAR_2, MOCK_NEW_CAR_3]),
            ({"model": "model_1"}, [MOCK_NEW_CAR_1, MOCK_NEW_CAR_2]),
            ({"model": "model_2"}, [MOCK_NEW_CAR_3]),
            ({"year": 2001}, [MOCK_NEW_CAR_1]),
            ({"year": 2002}, [MOCK_NEW_CAR_2, MOCK_NEW_CAR_3]),
            (
                {"color": "color_1"},
                [MOCK_NEW_CAR_1, MOCK_NEW_CAR_2, MOCK_NEW_CAR_3],
            ),
            ({"mileage": 1}, [MOCK_NEW_CAR_1, MOCK_NEW_CAR_2]),
            ({"mileage": 2}, [MOCK_NEW_CAR_3]),
            ({"price": 1}, [MOCK_NEW_CAR_1]),
            ({"price": 2}, [MOCK_NEW_CAR_2, MOCK_NEW_CAR_3]),
            ({"model": "wrong_model"}, []),
            ({"year": WRONG_YEAR}, []),
            ({"color": "wrong_color"}, []),
            ({"mileage": WRONG_MILEAGE}, []),
            ({"price": WRONG_PRICE}, []),
            ({"model": "model_1", "color": "wrong_color"}, []),
            ({"dealer_id": WRONG_DEALER_ID}, []),
            ({"id": WRONG_CAR_ID}, []),
        ],
    )
    def test_get_cars(
        self, testing_app, request_body, result, create_car_search_response
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        all_dealers = testing_app.post(url="/dealer/search", json={})
        dealer_1_id = all_dealers.json()[0]["id"]
        dealer_2_id = all_dealers.json()[1]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_1_id}
        )
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_2 | {"dealer_id": dealer_1_id}
        )
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_3 | {"dealer_id": dealer_2_id}
        )
        response = testing_app.post(url="/car/search", json=request_body)
        assert response.status_code == 200
        assert response.json() == create_car_search_response(*result)

    def test_get_car_by_dealer_id(
        self, testing_app, create_car_search_response
    ):

        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        response = testing_app.post(url="/dealer/search", json={})
        dealer_id = response.json()[0]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )
        response = testing_app.post(
            url="/car/search", json={"dealer_id": dealer_id}
        )
        assert response.json() == create_car_search_response(MOCK_NEW_CAR_1)

    def test_get_car_by_car_id(self, testing_app, create_car_search_response):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        response = testing_app.post(url="/dealer/search", json={})
        dealer_id = response.json()[0]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )
        response = testing_app.post(url="/car/search", json={})
        car_id = response.json()[0]["id"]
        response = testing_app.post(url="/car/search", json={"id": car_id})
        assert response.status_code == 200
        assert response.json() == create_car_search_response(MOCK_NEW_CAR_1)


class TestChangeCar:
    @pytest.mark.parametrize(
        ("request_body", "result"),
        [
            (
                {"model": "new_model"},
                {
                    "model": "new_model",
                    "year": 2001,
                    "color": "color_1",
                    "mileage": 1,
                    "price": 1.0,
                },
            ),
            (
                {"year": 2011},
                {
                    "model": "model_1",
                    "year": 2011,
                    "color": "color_1",
                    "mileage": 1,
                    "price": 1.0,
                },
            ),
            (
                {"color": "new_color"},
                {
                    "model": "model_1",
                    "year": 2001,
                    "color": "new_color",
                    "mileage": 1,
                    "price": 1.0,
                },
            ),
            (
                {"mileage": 2},
                {
                    "model": "model_1",
                    "year": 2001,
                    "color": "color_1",
                    "mileage": 2,
                    "price": 1.0,
                },
            ),
            (
                {"price": 2.0},
                {
                    "model": "model_1",
                    "year": 2001,
                    "color": "color_1",
                    "mileage": 1,
                    "price": 2.0,
                },
            ),
            (
                {
                    "model": "new_model",
                    "year": 2002,
                    "color": "new_color",
                    "mileage": 2,
                    "price": 2.0,
                },
                {
                    "model": "new_model",
                    "year": 2002,
                    "color": "new_color",
                    "mileage": 2,
                    "price": 2.0,
                },
            ),
            (
                {},
                {
                    "model": "model_1",
                    "year": 2001,
                    "color": "color_1",
                    "mileage": 1,
                    "price": 1.0,
                },
            ),
        ],
    )
    def test_change_car(
        self, testing_app, request_body, result, create_car_search_response
    ):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        response = testing_app.post(url="/dealer/search", json={})
        dealer_id = response.json()[0]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )
        response = testing_app.post(url="/car/search", json={})
        car_id = response.json()[0]["id"]
        response = testing_app.put(url=f"/car/{car_id}", json=request_body)
        assert response.status_code == 200
        assert response.json() == {"detail": "changed"}
        response = testing_app.post(url="/car/search", json={})
        assert response.json() == create_car_search_response(result)

    def test_change_car_when_car_does_not_exist(self, testing_app):
        wrong_car_id = 1
        response = testing_app.put(url=f"/car/{wrong_car_id}", json={})
        assert response.status_code == 404
        assert response.json() == {"detail": "car with this ID doesn't exist"}

    def test_change_car_dealer_when_dealer_does_not_exist(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        dealer = testing_app.post(url="/dealer/search", json={})
        dealer_id = dealer.json()[0]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )
        car = testing_app.post(url="/car/search", json={})
        car_id = car.json()[0]["id"]
        wrong_dealer_id = 2
        response = testing_app.put(
            url=f"/car/{car_id}", json={"dealer_id": wrong_dealer_id}
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "dealer with this ID doesn't exist"
        }

    def test_change_car_dealer(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_2)
        all_dealers = testing_app.post(url="/dealer/search", json={})
        dealer_1_id = all_dealers.json()[0]["id"]
        dealer_2_id = all_dealers.json()[1]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_1_id}
        )
        car = testing_app.post(url="/car/search", json={})
        car_id = car.json()[0]["id"]
        response = testing_app.put(
            url=f"/car/{car_id}", json={"dealer_id": dealer_2_id}
        )
        assert response.status_code == 200
        assert response.json() == {"detail": "changed"}
        car = testing_app.post(url="/car/search", json={})
        assert car.json()[0]["dealer_id"] == dealer_2_id


class TestDeleteCar:
    def test_delete_car(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        dealer = testing_app.post(url="/dealer/search", json={})
        dealer_id = dealer.json()[0]["id"]
        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )
        car = testing_app.post(url="/car/search", json={})
        car_id = car.json()[0]["id"]
        response = testing_app.delete(f"/car/{car_id}")
        assert response.status_code == 200
        assert response.json() == {"detail": "deleted"}

    def test_delete_car_when_car_does_not_exist(self, testing_app):
        wrong_car_id = 1
        response = testing_app.delete(f"/car/{wrong_car_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "car with this ID doesn't exist"}

    def test_delete_car_for_the_second_time(self, testing_app):
        testing_app.post(url="/dealer", json=MOCK_NEW_DEALER_1)
        dealer = testing_app.post(url="/dealer/search", json={})
        dealer_id = dealer.json()[0]["id"]

        testing_app.post(
            url="/car", json=MOCK_NEW_CAR_1 | {"dealer_id": dealer_id}
        )

        car = testing_app.post(url="/car/search", json={})
        car_id = car.json()[0]["id"]
        testing_app.delete(f"/car/{car_id}")
        response = testing_app.delete(f"/car/{car_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "car with this ID doesn't exist"}
