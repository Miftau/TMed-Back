from sqlalchemy.orm import Session
from app.models import user
from app.core.security import get_password_hash


def init_admin(db: Session):
    admin_email = "admin@healthapp.com"
    existing_admin = db.query(user.User).filter(user.User.email == admin_email).first()

    if not existing_admin:
        db_admin = user.User(
            full_name="Super Admin",
            email=admin_email,
            hashed_password=get_password_hash("Admin@123"),
            role=user.UserRole.admin,
            is_active=True,
        )
        db.add(db_admin)
        db.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin already exists.")
