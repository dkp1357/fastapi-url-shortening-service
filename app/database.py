from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(DATABASE_URL, echo=True)


# creates database and tables
def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
