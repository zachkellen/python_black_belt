from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.painting import Painting

@app.route('/paintings')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first')
        return redirect('/')
    paintings = Painting.get_all_paintings()
    my_paintings = Painting.get_my_paintings({'id': session['user_id']})
    return render_template('paintings.html', user_id = session['user_id'], first_name = session['first_name'], last_name = session['last_name'], paintings = paintings, my_paintings = my_paintings)

@app.route('/paintings/create')
def create_painting():
    if 'user_id' not in session:
        flash('Please login first')
        return redirect('/')
    return render_template('create.html')

@app.route('/paintings/submit', methods = ['post'])
def submit_painting():
    print(request.form)
    if Painting.painting_validator(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'quantity': int(request.form['quantity']),
            'user_id': session['user_id']
        }
        Painting.create_painting(data)
        return redirect('/paintings')
    return redirect('/paintings/create')

@app.route('/paintings/<int:painting_id>')
def view_painting(painting_id):
    if 'user_id' not in session:
        flash('Please login first', 'login')
        return redirect('/')
    data = {
        'id': painting_id
    }
    purchases = Painting.get_count(data)
    print('purchases are here')
    print(purchases)
    painting = Painting.get_painting_by_id(data)
    return render_template('view.html', painting = painting, purchases = int(purchases))

@app.route('/paintings/<int:painting_id>/edit')
def view_edit(painting_id):
    painting = Painting.get_painting_by_id({'id': painting_id})
    if painting.user_id != session['user_id']:
        flash('This is not your painting!')
        return redirect('/paintings')
    return render_template('edit.html', painting = painting)

@app.route('/paintings/<int:painting_id>/submit', methods=['POST'])
def submit_edit(painting_id):
    painting = Painting.get_painting_by_id({'id': painting_id})
    if painting.user_id != session['user_id']:
        flash('This is not your painting!')
        return redirect('/paintings')
    data = {
            'id': painting_id,
            'title': request.form['title'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'quantity': int(request.form['quantity'])
        }
    if Painting.painting_validator(data):
        Painting.update_painting(data)
        return redirect(f'/paintings/{painting_id}')
    flash('Edit not accepted.')
    return redirect(f'/paintings/{painting_id}/edit')

@app.route('/paintings/<int:painting_id>/delete')
def delete_painting(painting_id):
    painting = Painting.get_painting_by_id({'id': painting_id})
    if painting.user_id != session['user_id']:
        flash('This is not your painting!')
        return redirect('/paintings')
    if Painting.get_count({'id': painting_id}) > 0:
        Painting.delete_purchase({'id': painting_id})
        Painting.delete_painting({'id': painting_id})
        return redirect('/paintings')
    Painting.delete_painting({'id': painting_id})
    return redirect('/paintings')

@app.route('/paintings/<int:painting_id>/purchase', methods=['POST'])
def purchase_painting(painting_id):
    data = {'user_id': session['user_id'],
            'painting_id': painting_id
    }
    Painting.purchase_painting(data)
    return redirect('/paintings')