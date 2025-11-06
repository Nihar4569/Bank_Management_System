from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bank_Account(db.Model):
    __tablename__ = 'employee'
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(100), nullable=False)
    number = db.column(db.Integer, unique=True, nullable=False)
    balance = db.column(db.Float, nullable=False)

    def __repr__(self):
        return f'[Bank_Account {self.name} - {self.number} - {self.balance}]'
    
    
