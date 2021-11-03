from flask import Blueprint, flash, redirect, render_template, url_for

from .forms import CSVForm


bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = CSVForm()
    if form.validate_on_submit():
        flash('CSV is valid!', category='success')
        return redirect(url_for('views.index'))
    elif form.is_submitted():
        flash('Errors detected!', category='danger')

    return render_template('index.html', form=form)


@bp.route('/hello')
def hello():
    return 'hello'
