# Wolt assignment 2024 🚀
This is my solution for [Wolt Internship assignment 2024](https://github.com/woltapp/engineering-internship-2024).
I did project using FastAPI and [Kotlin Spring boot](https://github.com/mtoof/delivery-fee-calculator-kotlin).
```
├── Wolt-assignment-2024
│   ├── README.md
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Pipfile
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── consts.py
│   │   ├── calculation.py
│   │   ├── time_validation.py
│   ├── test/
│   │   ├── __init__.py
│   │   ├── test.py
```

I've put together this README with everyone in mind, aiming for simplicity and a user-friendly experience. I hope you find the information helpful.

## Data Validation 🛡️
I have used FastAPI for this aasignment, which is a modern , fast and straightforward framework for building APIs.
I have used Pydantic for data validation, which is a great library for data validation.
I've created a `CartItems` class `main.py` to ensure the integrity of our data using Pydantic's `BaseModel` class. This class is the backbone of our project, ensuring that all data is validated before being processed. 

Initially, I implemented my own data validation for handling user input. However, upon discovering Pydantic's robust data validation system, I was impressed with its capabilities. While I initially disagreed with using the 422 status code for indicating a user's bad request, favoring the 400 status code to indicate the problem is from the user's side, but I didn't want to change the default behavior of FastAPI. I also didn't want to use the `Depends` function to validate the data, as I wanted to keep the code as simple as possible.
For integer validation I used int = Field(..., gt=0) despite the fact that the task description didn't mention it, but I think it's a good idea to check if the quantity is greater than 0 because it's not logical to have negative or zero quantity in items like cart_value, delivery_distance or number_of_items.

I've also used `field_validator` decorator as @class_method to ensure that `time` item is always set to UTC and the format is always ISO format. As a little bonus I am checking if the `time` is set in to before the year 1999 as Finland joined the Euro zone in 1999.

### Model Validation Checks ✅

In the `field_validator`, I'm checking for:

- **Invalid datetime format:** Making sure the `time` is in ISO format.
I have moved the `time` validation to `time_validation.py` to make the code more readable.
- **Missing time zone:** Making sure the timezone exists in the JSON payload.
- **Timezone is not in UTC:** Checking if the `time` is set to UTC.
- **Time is before 1999:** Checking if the `time` is set in to before the year 1999 as Finland joined the Euro zone in 1999.

## Testing 🧪

Please check the `test` folder, I've lined up some handy test functions into `test.py` to ensure everything runs like a well-oiled machine.
I have created two functions to `setup_and_send_request` and `check_response`, which are used in the test functions to make the code more readable.
Each test function is testing a different scenario, and I've added a comment to each test function to explain what is being tested.
You can run the tests by running `pytest test/test.py -vv` in the root folder of the project.

## Project Usage 🚀

Ready to take this project for a spin? Just follow these simple steps:

## Development

Just make sure you are in the root folder of "My Assignment" and follow these steps to sets

### With Docker


#### Running the app
Run the app:
```
docker compose up
```

The API documentation is available in http://127.0.0.1:8000/docs.

#### Tests
```
docker compose run calculate_fee pytest test/test.py -vv
```


1. **Install Dependencies:**
If you have no virtual environment set up, you can create one using the following command:
#### Setting things up
Create a virtual environment:
- Install Pipenv: (recommended)
    
    ```bash
    pip install pipenv
    ```

- Install virtualenv:

    ```
    python -m venv .venv
    ```

Activate the virtual environment:

* Linux / MacOS:
    ```
    source .venv/bin/activate
    ```
* Windows (CMD):
    ```
    .venv/Scripts/activate.bat
    ```

* Windows (Powershell)
    ```
    .venv/Scripts/Activate.ps1
    ```
* For pipenv:
    ```
    pipenv shell
    ```
#### Installing dependencies
   - Using Pipenv (recommended):

     If you have Pipenv installed, navigate to the root folder using your terminal and execute the following commands to install the project dependencies:

     ```bash
     pipenv install      # It will Install all the project dependencies automatically
     ```

   - Using pip:

     If you don't have Pipenv installed, you can use `pip` to install the dependencies. Run the following command in the root folder:

     ```bash
     pip install -r requirements.txt
     ```

     This command installs the dependencies listed in the `requirements.txt` file.

2. **Run the application:**

   ```bash
    uvicorn app.main:app --reload
    ```
    The API documentation is available in http://127.0.0.1:8000/docs.

3. **Run the tests:**

    To kick off `test.py`, simply run this command if you're in the root of "My Assignment" folder:

    ```bash
    pytest test/test.py -vv
    ```

