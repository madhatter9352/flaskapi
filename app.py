from flask import Flask


app = Flask(__name__)


@app.route('/member')
def get_members():
    return 'returns all members'


@app.route('member/<int:member_id>')
def get_member(member_id):
    return 'Only one member'


@app.route('/member', methods = ['POST'])
def add_member():
    return 'This adds a new member'


@app.route('/member/<int:member_id>', methods = ['PUT', 'PATCH'])
def edit_member(member_id):
    return 'This edit a member'


@app.route('/member/<int:member_id>', methods = ['DELETE'])
def delete_member(member_id):
    return 'this delete a member'


if __name__ == '__main__':
    app.run(debug=True)