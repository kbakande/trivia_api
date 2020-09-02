import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# def retrieve_categories():
#   categories = Category.query.order_by(Category.id).all()
#   categories_list = [category.format() for category in categories]
#   return jsonify({
#       "categories" : categories_list
#       })

def pagination(request, QUESTIONS_PER_PAGE):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = Question.query.order_by(Question.id).all()
  questions_list = [question.format() for question in questions]
  paginated_questions = questions_list[start:end]

  categories = Category.query.order_by(Category.id).all()
  # categories_list = [category.format() for category in categories]
  categories_list = {category.id:category.type for category in categories}
  
  return jsonify({
    'questions': paginated_questions,
    'totalQuestions': len(questions_list),
    'categories' : categories_list,
    'currentCategory': None
    })




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources = {r"/*": {"origins" : "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allowed-Headers", "Content-Type, Authorization, true")
    response.headers.add("Access-Control-Allowed-Methods", "GET, PATCH, POST, DELETE, OPTIONS")
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()
    categories_list = {category.id:category.type for category in categories}

    return jsonify({
        "success": True,
        "categories" : categories_list
        })



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def getQuestions():

    result = pagination(request, QUESTIONS_PER_PAGE)

    return result

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      result = pagination(request, QUESTIONS_PER_PAGE)

      return result

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      req_body = request.get_json()

      new_question = req_body.get('question', None)
      new_answer = req_body.get('answer', None)
      new_difficulty = req_body.get('difficulty', None)
      new_category = req_body.get('category', None)

      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

      result = pagination(request, QUESTIONS_PER_PAGE)

      return result
    
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search_questions', methods=["POST"])
  def search_questions():
    body = request.get_json()
    
    searchTerm = body.get('searchTerm', None)
    if (not searchTerm) or (searchTerm is None):
      abort(404)
    searchTerm = "%{}%".format(searchTerm)

    try:
      searched_questions = Question.query.filter(Question.question.ilike(searchTerm)).all()
      search_list = [que.format() for que in searched_questions]

      return jsonify({
        "success": True,
        "questions": search_list,
        "totalQuestions": len(search_list),
        "currentCategory" : None
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def getByCategory(cat_id):
    try:
      cat_questions = Question.query.filter(Question.category==cat_id).all()
      catQuestionsList = [que.format() for que in cat_questions]

      if not catQuestionsList:
        abort(404)

      return jsonify({
        "questions" : catQuestionsList,
        "totalQuestions": len(catQuestionsList),
        "currentCategory": cat_id
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    body = request.get_json()
    cat_id = body['quiz_category']['id']
    prev_ques = body['previous_questions'] 

    try:
      if cat_id == 0:
        questions = Question.query.all()
        que_list = [que.format() for que in questions]
      else: 
        questions = Question.query.filter(Question.category == cat_id)
        que_list =[que.format() for que in questions]
     
      if len(que_list) == 0:
        abort(404)

      random.shuffle(que_list)
      currentQuestion = None
      for que in que_list:
        if que['id'] not in prev_ques:
          currentQuestion = que
          break
      return jsonify({
        'success': True,
        'previousQuestions': body['previous_questions'],
        'question': currentQuestion
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  return app

    