from fastapi import FastAPI, HTTPException   # importamos libreria para manejar las excepciones HTTP
from pydantic import BaseModel  # libreria para llevar a cabo validación de datos
from typing import Optional, Text  # a partir de Python 3.5 se añade el módulo typing a la librería estándar, para permitir anotar los tipos de forma nativa (PEP 484).
from datetime import datetime   # El módulo datetime proporciona clases para manipular fechas y horas. 
from uuid import uuid4 as uuid   # Libreria para generar un ID

app = FastAPI()         # inicializamos fastapi

posts = []     # creamos un array en memoria para simular la base de datos

# Post model creado usando la libreria pydantic
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime =  datetime.now()
    published_at: Optional[datetime] 
    published: Optional[bool] = False  # creamos variable o bandera que nos diga si esta publicado o no

@app.get('/')    # endpoint que apunta a la raiz del proyecto
def read_root():
    return {"welcome": "Zona raiz del proyecto"}


@app.get('/posts')    # endpoint que apunta a traer los registros del array post
def get_posts():
    return posts


@app.post('/posts')     # endpoint para crear nuevos posts
def save_post(post: Post):   # decimos que es de tipo Post como la clase
    #print(post)       # imprimimos valores en consola
    #print(post.dict())   # imprimimos valores en consola como un diccionario
    #return "recibido"      # retorno
    post.id = str(uuid())   # antes de guardarlo generamos en ID aleatorio y lo convertimos a string
    print(uuid())
    posts.append(post.dict())   # convirte los valores en un diccionario y los añade a la lista
    return posts[-1]       # me devuelve la ultima publicacion añadida


@app.get('/posts/{post_id}')    # endpoint para listar post por ID
def get_post(post_id: str):
    #print(post_id)
    #return "Recibido"
    for post in posts:   # se recorren todos los posts
        if post["id"] == post_id:   # si existe la publicacion o post
            return post      # retornamos el post por su ID
    raise HTTPException(status_code=404, detail="Item not found")  # retornamos 404 si no lo encontramos


@app.delete('/posts/{post_id}')   # endpoint para eliminar un post
def delete_post(post_id: str):
    for index, post in enumerate(posts):   # se busca el indice del post a eliminar
        #print(post)
        #print(index)
        #return "Recibido"
        if post["id"] == post_id:  # si se encuentra el post a eliminar
            posts.pop(index)   # Eliminar post de la lista o array
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")  # se devuelve codigo de error http


@app.put('/posts/{post_id}')   # endpoint para actualizar
def update_post(post_id: str, updatedPost: Post):  # recibimos el id del post a actualizar y una publicacion actualizada para reemplazar los campos
    for index, post in enumerate(posts):  # recorremos los post
        if post["id"] == post_id:  # si lo encontramos
            posts[index]["title"]= updatedPost.dict()["title"]   # reemplazamos cada atributo
            posts[index]["content"]= updatedPost.dict()["content"]
            posts[index]["author"]= updatedPost.dict()["author"]
            return {"message": "Post has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")