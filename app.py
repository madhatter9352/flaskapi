from flask import Flask, g, request, jsonify
from database import connect_db, get_bd


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/members')
def get_members():
    return 'returns all members'


@app.route('/member/<int:member_id>')
def get_member(member_id):
    return 'Only one member'


@app.route('/member', methods = ['POST'])
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
def edit_member(member_id):
    return 'This edit a member'


@app.route('/member/<int:member_id>', methods = ['DELETE'])
def delete_member(member_id):
    return 'this delete a member'


if __name__ == '__main__':
    app.run(debug=True)