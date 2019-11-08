from flask import Flask,g,request,jsonify
from dabatabe import get_db
from functools import wraps
app = Flask(__name__)
api_username = 'rajendra'
api_password = 'rajendra'

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_password and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'authontication failed!'}),403
    return decorated

# data base connetions
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()
# geting the data for api
@app.route('/member',methods = ['GET'])
@protected
def get_members():
    db = get_db()
    member_cur = db.execute('select id, name, email, level from members')
    members = member_cur.fetchall()

    return_values = []

    for member in members:
        member_dict = {}
        member_dict['id'] = member['id']
        member_dict['name'] = member['name']
        member_dict['email'] = member['email']
        member_dict['level'] = member['level']

        return_values.append(member_dict)
    return jsonify({'members' : return_values})

# getting only one user data with id
@app.route('/member/<int:member_id>', methods = ['GET'])
@protected
def get_member(member_id):
    db = get_db()
    member_cur = db.execute('select id, name, email, level from members where id = ?',[member_id])
    member = member_cur.fetchone()
    return jsonify({'member' : {'id':member['id'],'name':['name'],'email': member['email'],'level':member['level']}})

# inserting the values into the database
@app.route('/member',methods = ['POST'])
@protected
def add_member():
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    db = get_db()
    db.execute('insert into members( name,email,level) values(?,?,?)',[name, email,level])
    db.commit()

    mumber_cur = db.execute('select id, name, email, level from members where name = ?',[name])
    new_mumber = mumber_cur.fetchone()
    return jsonify({'members':{'id':new_mumber['id'], 'name': new_mumber['name'],'email':new_mumber['email'], 'level':new_mumber['level']}})
# update the data with user id
@app.route('/member/<int:member_id>',methods = ['PUT','PATCH'])
@protected
def edit_member(member_id):
    new_number_data = request.get_json()
    name = new_number_data['name']
    email = new_number_data['email']
    level = new_number_data['level']
    db = get_db()
    db.execute('update members set name = ?, email = ?, level = ? where id = ?',[name, email, level, member_id])
    db.commit()
    member_cur = db.execute('select id , name, email, level from members where id = ?',[member_id])
    new_number = member_cur.fetchone()
    return jsonify({'membres': { 'id' : new_number['id'], 'name' : new_number['name'], 'email': new_number['email'],'level': new_number['level'] }})

# delete the user data with id..
@app.route('/member/<int:member_id>',methods = ['DELETE'])
@protected
def delete_member(member_id):
    db = get_db()
    db.execute('delete from members where id = ?',[member_id])
    db.commit()
    return jsonify('{Message: The member has been deleted!}')
if __name__ == '__main__':
    app.run(debug=True)