# project/api/views.py


from flask import Blueprint, jsonify, request

from project.api.models import User, Kanji, Entry, Reading, ReadingInfo, Meaning
from project import db
from sqlalchemy import exc


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong!'
	})

@users_blueprint.route('/users', methods=['POST'])
def add_user():
	post_data = request.get_json()
	if not post_data:
		response_object = {
			'status': 'fail',
			'message': 'Invalid payload.'
		}
		return jsonify(response_object), 400
	username = post_data.get('username')
	email = post_data.get('email')
	try:
		user = User.query.filter_by(email=email).first()
		if not user:
			db.session.add(User(username=username, email=email))
			db.session.commit()
			response_object = {
				'status': 'success',
				'message': f'{email} was added!'
			}
			return jsonify(response_object), 201
		else:
			response_object = {
				'status': 'fail',
				'message': 'Sorry. That email already exists.'
			}
			return jsonify(response_object), 400
	except exc.IntegrityError as e:
		db.session.rollback()
		response_object = {
			'status': 'fail',
			'message': 'Invalid payload.'
		}
		return jsonify(response_object), 400

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
	""" Get single user details """
	response_object = {
		'status': 'fail',
		'message': 'User does not exist'
	}
	try:
		user = User.query.filter_by(id=int(user_id)).first()
		if not user:
			return jsonify(response_object), 404
		else:
			user = User.query.filter_by(id=user_id).first()
			response_object = {
				'status': 'success',
				'data': {
					'username': user.username,
					'email': user.email,
					'created_at': user.created_at
				}
			}
			return jsonify(response_object), 200
	except ValueError:
		return jsonify(response_object), 404

@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
	""" Get all users """
	users = User.query.all()
	users_list = []
	for user in users:
		user_object = {
			'id': user.id,
			'username': user.username,
			'email': user.email,
			'created_at': user.created_at
		}
		users_list.append(user_object)
	response_object = {
		'status': 'success',
		'data': {
			'users': users_list
		}
	}
	return jsonify(response_object), 200

def get_single_kanji(kanji_hexa):
	""" Get Kanji details from hexadecimal code """
	response_object = {
		'status': 'fail',
		'message': 'Kanji does not exist'
	}

	try:
		entry = Entry.query.filter_by(seq=int(kanji_hexa,16)).first() #int(kanji,id, 16) converts hexadecimal to decimal
		response_object2 = {
			'status': 'fail',
			'message': 'Kanji does not exist',
			'codigo': int(kanji_hexa,16)
		}
		if not entry:
			return jsonify(response_object2), 404
		else:
			#kanji = Kanji.query.filter_by(entr=kanji_hexa).first()
			#db.session.query(kanji.txt, entry.).\
    		#	join(Account, Account.organization == User.organization).\
    		#	filter(Account.name == 'some name')
			kanji = Kanji.query.filter_by(entr=int(entry.id)).first()
			readings = Reading.query.order_by(Reading.rdng.asc()).filter_by(entr=int(kanji.entr)).all()
			readingsinfo = ReadingInfo.query.order_by(ReadingInfo.rdng.asc()).filter_by(entr=int(kanji.entr)).all()
			joint = db.session.query(ReadingInfo.kw, Reading.txt).\
				join(Reading, Reading.entr == ReadingInfo.entr).\
				filter(Reading.entr == kanji.entr).distinct()
			all_readings = []
			readings_on = []
			readings_kun = []
			for i in range(len(readings)):
				if readingsinfo[i].kw == 128:
					readings_on.append(readings[i].txt)
				if readingsinfo[i].kw == 106:
					readings_kun.append(readings[i].txt)

			meanings = Meaning.query.order_by(Meaning.gloss.asc()).filter_by(entr=int(kanji.entr)).all()
			meanings_list = []
			for meaning in meanings:
				meanings_list.append(meaning.txt)

			response_object = {
				'status': 'success',
				'data': {
					'id': entry.id,
					'kanji': kanji.txt,
					'decimal': entry.seq,
					'hexadecimal': kanji_hexa,
					'readings': {
						'onyomi': readings_on,
						'kunyomi': readings_kun
					},
					'meanings': meanings_list
				}
			}
			return jsonify(response_object), 200
	except ValueError:
		return jsonify(response_object), 404

@users_blueprint.route('/kanji/<kanji_char>', methods=['GET'])
def get_single_kanji_char(kanji_char):
	""" Get Kanji details from Kanji character """
	for _c in kanji_char:
		hexa_code = ('%04x' % ord(_c))
	return get_single_kanji(hexa_code.upper())

@users_blueprint.route('/hexa/<kanji_hexa>', methods=['GET'])
def get_single_kanji_hext(kanji_hexa):
	""" Get Kanji details from hexadecimal code """
	return get_single_kanji(kanji_hexa.upper())
