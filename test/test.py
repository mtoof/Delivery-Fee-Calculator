from fastapi.testclient import TestClient
from app.main import app
from app import consts

def setup_and_send_request(client, cart_value, delivery_distance, number_of_items,time):
	'''
		Setup the request and send it to the server.
	'''
	data = {
			"cart_value": cart_value,
			"delivery_distance": delivery_distance,
			"number_of_items": number_of_items,
			"time": time
	}
	response = client.post(consts.URL, json=data)
	return response

def check_response(response, expected_status_code, expected_response, error_message = None):
	'''
		Check the response from the server.
		if the expected_response is -1, it means that I don't care about the details because I'm expecting an error.
	'''
	assert response.status_code == expected_status_code
	if expected_response >= 0:
		assert response.json() == {"delivery_fee": expected_response}
	if error_message:
		assert response.json() == {"detail": error_message}

def test_no_json_payload():
	'''No JSON payload'''
	with TestClient(app) as client:
		response = client.post(consts.URL)

	assert response.status_code == 422

def test_correct_payload():
	'''
		correct JSON payload
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 790, 2235,4, "2024-02-21T14:40:00Z")
		check_response(response, 200, 710)

	'''
		correct JSON payload
	'''
	with TestClient(app) as client:
		response =  setup_and_send_request(client, 1, 1000, 4, "2024-02-21T14:40:00Z")
		check_response(response, 200, 1199)

	'''
		correct JSON payload
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 12700, 1000, 4, "2024-02-21T14:40:00Z")
		check_response(response, 200, 200)


def test_incorrect_data():
	'''
		incorrect delivery_distance name in JSON payload
	'''
	with TestClient(app) as client:
		data = {
			"cart": 790,
			"delivery": 2235,
			"number_of_items": 4,
			"time": "2024-02-21T14:40:00Z"
		}
		response = client.post(consts.URL, json=data)
		check_response(response, 422, -1)


def test_less_than_zero_values():
	'''
		incorrect delivery_distance name in JSON payload
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 0, -2235,4, "2024-02-21T14:40:00Z")
		check_response(response, 422, -1)

def test_correct_data_extra_items():
	'''
 		correct JSON payload for extra items
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 790, 2235,20, "2024-02-21T14:40:00Z")
		check_response(response, 200, 1500)

def test_correct_data_no_delivery_fee():
	'''
 		correct JSON payload for 200 euros or more in cart_value
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 20000, 2235,20, "2024-02-21T14:40:00Z")
		check_response(response, 200, 0)

	with TestClient(app) as client2:
		response = setup_and_send_request(client2, 21000, 2235,20, "2024-03-21T14:40:00Z")
		check_response(response, 200, 0)

def test_missing_items():
	'''
 		correct JSON payload for a couple of items are missing
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 21000, None,None, "2024-03-21T14:40:00Z")
		check_response(response, 422, -1)

def test_incorrect_timezone():
	'''
		incorrect timezone
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 21000, 2235,20, "2024-03-21T14:40:00+02:00")
		check_response(response, 400, -1, "Datetime is not in UTC.")

def test_past_date():
	'''
		past_date
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 21000, 2235,20, "1995-03-21T14:40:00Z")
		check_response(response, 400, -1, "Item 'time' is invalid, Year can't be less than 1999")

def test_missing_time_zone():
	'''
 		test missing timezone
	'''
	with TestClient(app) as client:
		response = setup_and_send_request(client, 21000, 2235,20, "1995-03-21T14:40:00")
		check_response(response, 400, -1, "item 'time' is invalid, time zone is missing")
	