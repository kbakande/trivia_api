import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import random

from models import setup_db, db, Question, Category

migrate = Migrate()

QUESTIONS_PER_PAGE = 10

def pagination(request, QUESTIONS_PER_PAGE):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = Question.query.order_by(Question.id).all()
  questions_list = [question.format() for question in questions]
  paginated_questions = questions_list[start:end]
  categories = Category.query.order_by(Category.id).all()
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
  migrate.init_app(app, db)

  CORS(app, resources = {r"/*": {"origins" : "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allowed-Headers", "Content-Type, Authorization, true")
    response.headers.add("Access-Control-Allowed-Methods", "GET, PATCH, POST, DELETE, OPTIONS")
    return response

  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()
    categories_list = {category.id:category.type for category in categories}
    return jsonify({
        "success": True,
        "categories" : categories_list
        })

  @app.route('/questions')
  def getQuestions():
    result = pagination(request, QUESTIONS_PER_PAGE)
    return result

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      result = pagination(request, QUESTIONS_PER_PAGE)
      result = result.get_json()
      return jsonify({
        "success": True,
        "deleted_id": question_id,
        "questions": result["questions"],
        "totalQuestions": result["totalQuestions"]
      })
    except:
      abort(422)

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
      result = result.get_json()
      return jsonify ({
        "success": True,
        "created_id":question.id,
        "questions": result["questions"],
        "totalQuestions": result["totalQuestions"]
      })
    except:
      abort(422)

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

  @app.route('/categories/<int:cat_id>/questions')
  def getByCategory(cat_id):
    try:
      cat_questions = Question.query.filter(Question.category==cat_id).all()
      catQuestionsList = [que.format() for que in cat_questions]
      if not catQuestionsList:
        abort(404)
      return jsonify({
        "success": True,
        "questions" : catQuestionsList,
        "totalQuestions": len(catQuestionsList),
        "currentCategory": cat_id
      })
    except:
      abort(422)

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

    