from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели базы данных
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    reviews = db.relationship('Review', backref='book', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

# Главная страница с книгами и поиском
@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '').strip()  # Получаем поисковый запрос
    if search_query:
        # Поиск по названию книги без учета регистра
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    else:
        books = Book.query.all()  # Если запрос пуст, показываем все книги
    
    return render_template('index.html', books=books)

# Страница книги с отзывами
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        stars = request.form['stars']
        new_review = Review(name=name, comment=comment, stars=stars, book_id=book.id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('book', book_id=book.id))

    reviews = Review.query.filter_by(book_id=book.id).all()
    return render_template('book.html', book=book, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)

# Добавление начальных данных
"""
with app.app_context():
    db.create_all()

    # Добавление начальных книг, если база данных пуста
    if not Book.query.first():  # Проверяем, есть ли уже книги в базе данных
        books = [
            Book(title="1984", description="Роман-антиутопия Джорджа Оруэлла о тоталитарном режиме."),
            Book(title="Властелин колец", description="Эпическая трилогия Дж. Р. Р. Толкина о путешествии хоббитов и борьбе с темным властелином."),
            Book(title="Хоббит", description="Приключенческая повесть Дж. Р. Р. Толкина, рассказывающая историю Бильбо Бэггинса и его путешествия."),
            Book(title="Самый богатый человек в Вавилоне", description="Книга Джорджа С. Клейсона с мудрыми наставлениями и советами по личным финансам, основанными на древнем вавилонском опыте."),
            Book(title="Слова назидания", description="Сборник философских размышлений Абая Кунанбаева о жизни, морали, воспитании и внутреннем росте человека.")
        ]
        db.session.add_all(books)
        db.session.commit()
"""
