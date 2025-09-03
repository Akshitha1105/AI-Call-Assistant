from app.db import engine, Base
from app import models


def main():
    Base.metadata.create_all(bind=engine)
    print("DB initialized")


if __name__ == "__main__":
    main()

