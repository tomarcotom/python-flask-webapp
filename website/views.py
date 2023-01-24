from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  if request.method == 'POST':
    if request.form.get('delete-note'):
      delete_note(request.form.get('delete-note')) # note.id
      return redirect(url_for("views.home", user=current_user))
    if request.form.get('add-note'):
      add_note(request.form.get('note'))
      return redirect(url_for("views.home", user=current_user))

  return render_template("home.html", user=current_user)

def add_note(note):
  new_note = Note(text=note, user_id=current_user.id)
  db.session.add(new_note)
  db.session.commit()
  flash('Note added!', category='success')

def delete_note(noteId):
  note = Note.query.get(noteId)
  if note and note.user_id == current_user.id:
    db.session.delete(note)
    db.session.commit()
    flash('Note removed!', category='success')