# Imports
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, NVARCHAR

# Initialising app

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
Bootstrap(app)

# Create database using SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///GoblinCakes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create Table in database using SQLAlchemy


class GoblinCakeSales(db.Model):
    __tablename__ = "GoblinCakeSales"
    id = Column(Integer, primary_key=True, nullable=False)
    Product = Column(NVARCHAR, nullable=True)
    Product_Type = Column(NVARCHAR, nullable=True)
    Price_Per = Column(Integer, nullable=True)
    Units_Sold = Column(Integer, nullable=True)
    Quarter = Column(Integer, nullable=True)


db.create_all()

# Create nested list using data

product_data = [['Hobgoblin', 'Cake', 4, 388, 1],
                ['Green Goblin', 'Cake', 4, 312, 1],
                ['Forest Sprite', 'Canned Drink', 0.8, 97, 1],
                ['Redcap', 'Cake', 3.5, 605, 1],
                ['Imp', 'Cake', 2, 162, 1],

                ['Hobgoblin', 'Cake', 4, 482, 2],
                ['Green Goblin', 'Cake', 4, 312, 2],
                ['Forest Sprite', 'Canned Drink', 0.8, 123, 2],
                ['Redcap', 'Cake', 4, 401, 2],
                ['Imp', 'Cake', 1.5, 540, 2],
                ['Filthy Hobbit', 'Cookie', 1, 325, 2],

                ['Hobgoblin', 'Cake', 4, 389, 3],
                ['Green Goblin', 'Cake', 4, 302, 3],
                ['Forest Sprite', 'Canned Drink', 0.8, 168, 3],
                ['Redcap', 'Cake', 4, 433, 3],
                ['Imp', 'Cake', 2, 486, 3],
                ['Filthy Hobbit', 'Cookie', 1, 164, 3],
                ['Wretched Elf', 'Cookie', 1, 212, 3],
                ['Foul Dwarf', 'Cookie', 1, 168, 3],
                ['Vile Human', 'Cookie', 1, 92, 3],

                ['Hobgoblin', 'Cake', 4, 369, 4],
                ['Green Goblin', 'Cake', 4, 333, 4],
                ['Forest Sprite', 'Canned Drink', 0.8, 168, 4],
                ['Redcap', 'Cake', 4, 462, 4],
                ['Imp', 'Cake', 2, 501, 4],
                ['Filthy Hobbit', 'Cookie', 1, 125, 4],
                ['Wretched Elf', 'Cookie', 1, 201, 4],
                ['Foul Dwarf', 'Cookie', 1, 162, 4],
                ['Vile Human', 'Cookie', 1, 143, 4],
                ['Wizard Spit', 'Hot Drink', 3.5, 455, 4],
                ['Brownie', 'Cake', 1.5, 666, 4]
                ]

# Check if data is already in database

if GoblinCakeSales.query.all():
    pass
else:
    # Add data to database if empty
    for product in product_data:
        new_product = GoblinCakeSales(
            Product=product[0],
            Product_Type=product[1],
            Price_Per=product[2],
            Units_Sold=product[3],
            Quarter=product[4]
        )
        db.session.add(new_product)
        db.session.commit()

# Create global variables
just_cakes = True
quarter = 1

# Display data on page


@app.route("/", methods=["GET", "POST"])
def index():
    global just_cakes
    global quarter
    # Get data from db
    sales_data = GoblinCakeSales.query.all()

    # Form for changing quarter
    if request.method == "POST" and request.form.get("value"):
        quarter = int(request.form.get("value"))
        return render_template("index.html", sales_data=sales_data, quarter=quarter, just_cakes=just_cakes)

    # Form for toggling Cakes Only
    elif request.method == "POST":
        if just_cakes:
            just_cakes = False
        else:
            just_cakes = True
        return render_template("index.html", sales_data=sales_data, just_cakes=just_cakes, quarter=quarter)

    return render_template("index.html", sales_data=sales_data, just_cakes=just_cakes)


if __name__ == "__main__":
    app.run()
