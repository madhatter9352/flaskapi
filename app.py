from flask import Flask, g, request, jsonify
from database import connect_db, get_bd
from functools import wraps


app = Flask(__name__)

api_username = 'admin'
api_password = 'admin'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'unauthorized'}), 401
    return decorated


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/members')
@protected
def get_members():
    db = get_bd()
    members_curs = db.execute("select * from members order by id")
    members_reslt = members_curs.fetchall()

    return_values = []

    for member in members_reslt:
        member_dict = {}
        member_dict['id'] = member['id']
        member_dict['name'] = member['name']
        member_dict['email'] = member['email']
        member_dict['level'] = member['level']

        return_values.append(member_dict)

    return jsonify({ 'members': return_values })


@app.route('/member/<int:member_id>')
@protected
def get_member(member_id):
    db = get_bd()
    member_cursor = db.execute("select * from members where id = ?", [member_id])
    member_result = member_cursor.fetchone()

    return jsonify({ 'id': member_result['id'],
                     'name': member_result['name'],
                     'email': member_result['email'],
                     'level': member_result['level']
                     })


@app.route('/member', methods = ['POST'])
@protected
def add_member():
    if request.method == 'POST':
        member_data = request.get_json()
        name = member_data['name']
        email = member_data['email']
        level = member_data['level']

        db = get_bd()
        db.execute("insert into members(name, email, level) values(?, ?, ?)", [name, email, level])
        db.commit()

        member_cur = db.execute("select * from members where name = ?", [name])
        new_member_check = member_cur.fetchone()

        return jsonify({ 'id': new_member_check['id'], 'name': new_member_check['name'],
                        'email': new_member_check['email'], 'level': new_member_check['level'] })

    return 'This adds a new member'


@app.route('/member/<int:member_id>', methods = ['PUT', 'PATCH'])
@protected
def edit_member(member_id):
    db = get_bd()

    member_data = request.get_json()
    name = member_data['name']
    email = member_data['email']
    level = member_data['level']

    db.execute("update members set name = ?, email = ?, level = ? where id = ?", [name, email, level, member_id])
    db.commit()

    member_cursor = db.execute("select * from members where id = ?", [member_id])
    member_result = member_cursor.fetchone()

    return jsonify({ 'id': member_id,
                     'name': member_result['name'],
                     'email': member_result['email'],
                     'level': member_result['level']
                     })


@app.route('/member/<int:member_id>', methods = ['DELETE'])
@protected
def delete_member(member_id):
    db = get_bd()
    db.execute("delete from members where id = ?", [member_id])
    db.commit()

    return 'delete successfully'


if __name__ == '__main__':
    app.run(debug=True)