# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.  

### API Reference

### Getting Started

* BASE URL: The trivia_app is not hosted on any URL at the moment. However, it can be run locally
* This version of the application does not require authentication

### Error Handling

Errors are returned as JSON objects in the following formats:

```json
{ 
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return two types of errors when a request fails:

* 404: Request Not Found
* 422: Unprocessable

### Endpoints

GET /categories
* General
    - Returns an object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    - Request Arguments: Results are paginated in groups of 10. Include an optional request argument to specify page number, starting from 1
* Sample: ''' curl 127.0.0.1:5000/categories '''

```json
{
   "categories":{
      "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
   },
   "success":true
}
```

GET /questions
* General
    - Return a dictionary with 4 keys representing categories, currentCategory, questions and totalQuestions. Categories is a object, current category is null, questions is a list of question objects while totalQuestions is an integer indicating the number of questions 
    - Request Arguments: Results are paginated in groups of 10. Include an optional request argument to specify page number, starting from 1
* Sample: ''' curl 127.0.0.1:5000/questions?page=1'''

```json
{
   "categories":{
      "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
   },
   "currentCategory":null,
   "questions":[
      {
         "answer":"Maya Angelou",
         "category":4,
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }
   ],
   "totalQuestions":1
}
```

DELETE /questions/{question_id}
* General
    - Deletes the question of the given id if it exists. Returns the id of the deleted question, success value, total questions and questions list 
      based on the current page number to update the frontend.

* Sample: 'curl -X DELETE http://127.0.0.1:5000/questions/16?page=2'

```json
{
  "deleted_id": "13",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```


POST /questions
* General
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend.

* Sample: 'curl -X POST -H "Content-Type: application/json" -d '{"answer":"Barack Obama","category":4,"difficulty":1,"question":"Who is the first Black US president?"}' http://127.0.0.1:5000/questions?page=1' 

```json
{
  "created_id": 53,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "totalQuestions": 5
}
```

POST /search_questions
* General
    - Retrieves questions based on a search term submitted by the client. Returns a list of questions matching the search term to be displayed on the frontend, success value, total questions and the current category which is null.

* Sample: 'curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}' http://127.0.0.1:5000/search_questions' 

```json
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
```

GET /categories/{category_id}/questions
* General
    - Retrieves questions corresponding to the category id. Returns a list of questions matching the category id, success value, total number questions in the category and the current category.

* Sample: 'curl http://127.0.0.1:5000/categories/1/questions' 

```json
{
  "currentCategory": 5,
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

POST /quizzes
* General
    - Retrieves questions based on the submitted category_id and list of previous questions' ids. Returns a list of questions matching the category id and not in the previous questions, succes value and the list of previous questions' ids.

* Sample: 'curl -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"id": 5}, "previous_questions": []}' http://127.0.0.1:5000/quizzes' 

```json
{
  "previousQuestions": [],
  "question": {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  "success": true
}
```
## Testing
To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```





Indoor Air Quality Meters Market by Product and Geography - Forecast and Analysis 2020-2024
