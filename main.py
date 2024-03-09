from fastapi import FastAPI
from fastapi import FastAPI, Body, Response, status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# request Get method url: "/"

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title" : "title of post1", "content" : "content of post 1", "id" : 1}, {"title" : "favorite food", "content": "i like pizza", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in  enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"messsage" : "Welcome to my API"}

@app.get("/new_posts")
def get_posts():
    return {"data" : my_posts}

@app.get("/post/add")
def math():
    return {"addtion" : "additoion of two number"}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

# Api will check the all the latest update so make sure that the posts/{id} will able to matches to the "posts/latest"

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) -1]
#     return {"detail": post}



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id: {id} was not found"}
    return {"post_detail" : f"Here is the post {id}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    # delete post
    # find the index in the array that has required Id
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id : int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'message': "updated post"}