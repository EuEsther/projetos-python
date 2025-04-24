from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from datetime import datetime
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
hashids = Hashids(min_length=4, salt="seu_salt_secreto")


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["url"]
        custom_slug = request.form.get("custom_slug", "").strip()

        # Validação da URL
        if not original_url.startswith(("http://", "https://")):
            original_url = "http://" + original_url

        # Lógica para slug personalizado
        if custom_slug:
            if not re.match(r"^[a-zA-Z0-9_-]+$", custom_slug):
                return "Slug inválido! Use apenas letras, números, '-' ou '_'", 400

            # Verifica se o slug personalizado JÁ EXISTE no banco
            if URL.query.filter_by(short_code=custom_slug).first():
                return "Este slug já está em uso. Escolha outro.", 400

            # Cria a URL com o slug personalizado
            new_url = URL(
                original_url=original_url,
                short_code=custom_slug,
            )
            db.session.add(new_url)
            db.session.commit()
            short_code = custom_slug

        # Lógica para slug automático (se não houver custom_slug)
        else:
            existing_url = URL.query.filter_by(original_url=original_url).first()
            if existing_url:
                short_code = existing_url.short_code
            else:
                new_url = URL(original_url=original_url, short_code="")
                db.session.add(new_url)
                db.session.commit()
                short_code = hashids.encode(new_url.id)
                new_url.short_code = short_code
                db.session.commit()

        return render_template(
            "index.html",
            short_url=f"{request.host_url}{short_code}",
            original_url=original_url,
        )

    return render_template("index.html")


@app.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)
    return "URL não encontrada", 404

@app.route('/stats/<short_code>')
def stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return render_template(
        'stats.html',
        url=url,
        short_url=f"{request.host_url}{url.short_code}"
        )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
