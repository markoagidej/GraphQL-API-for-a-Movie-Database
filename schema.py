import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel, db, Genre as GenreModel
from sqlalchemy.orm import Session

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    def resolve_movies(self, info):
        return db.session.execute(db.select(MovieModel)).scalars()
    
    # get_movies_by_genre = graphene.List(Movie)
    # def resolve_get_movies_by_genre(self, info, id):
    #     # class Arguments:
    #     #     id = graphene.Int(required=True)

    #     return db.session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars()
    
class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_id = graphene.Int(required=False)

    movie = graphene.Field(Movie)

    def mutate(self, info, title, director, year, **kwargs):
        with Session(db.engine) as session:
            with session.begin():
                movie = MovieModel(title=title, director=director, year=year)
                if kwargs.get('genre_id', None):
                    genre = session.query(Genre).filter_by(id=f'{kwargs['genre_id']}').first()
                    if genre:
                        movie.append(genre)
                session.add(movie)

            session.refresh(movie)
            return AddMovie(movie=movie)
        
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, director, year, genre_id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.director = director
                    movie.year = year
                    movie.genre = session.query(Genre).filter_by(id=f'{genre_id}').first()
                else:
                    return None
            session.refresh(movie)
            return UpdateMovie(movie=movie)

class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    session.delete(movie)
                else:
                    return None
            session.refresh(movie)
            return DeleteMovie(movie=movie)

    
class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        with Session(db.engine) as session:
            with session.begin():
                genre = GenreModel(name=name)
                session.add(genre)

            session.refresh(genre)
            return AddGenre(genre=genre)
        
class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id, name):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                    genre.name = name
                else:
                    return None
            session.refresh(genre)
            return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                    session.delete(genre)
                else:
                    return None
            session.refresh(genre)
            return DeleteGenre(genre=genre)
        
class Mutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()
    create_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()