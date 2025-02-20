from sqlalchemy.orm import Session
import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, calories=product.calories)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()