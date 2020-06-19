# SimpleCMS

![Django CI](https://github.com/seladb/SimpleCMS/workflows/Django%20CI/badge.svg)

This example project demonstrates the integration between Django and GraphQL.
It implements a very simple Content Management System (CMS) that allows creation of blog posts and adding likes and comments to them.

The project uses [Django](https://www.djangoproject.com/) and [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/) as Backend and *TODO* as a Frontend.

*NOTE: this example requires Python 3.7 or later*

## Installation

This project can be run locally or using [Docker Compose](https://docs.docker.com/compose/).

### Run locally

Clone the repo:

```shell
git clone https://github.com/seladb/SimpleCMS
```

Create a local `virtualenv` environment:

```shell
virtualenv venv
```

Install dependencies:

```shell
pip install -r requirements.txt
```

Create admin user (required on first run only):

```shell
./create-admin-local.sh
```

Run migrations and start server:

```shell
./run-local.sh
```

Alternatively you can run migrations and start the server separately:

```shell
python manage.py migrate
```

```shell
python manage.py runserver
```

### Run using Docker Compose

Make sure Docker and Docker Compose are installed.

Clone the repo:

```shell
git clone https://github.com/seladb/SimpleCMS
```

Create admin user (required on first run only):

```shell
./create-admin-docker.sh
```

Run Docker Compose:

```shell
./run-docker.sh
```

### Accessing the server

Post installation the server will be available via this URL: <http://127.0.0.1:8000/>

There are two views currently available:

- Admin view: <http://127.0.0.1:8000/admin/>
- GraphiQL view: <http://127.0.0.1:8000/graphql/>

### Run tests

To run the unit-tests please execute the following command:

```shell
python manage.py test
```

## GraphQL queries and mutations

This example project exposes the following GraphQL queries and mutations. Before running these examples in [GraphiQL web-view](http://127.0.0.1:8000/graphql/) please create users via [Django Admin interface](http://127.0.0.1:8000/admin/)

- Get all blog posts currently available in the database:

  ```graphql
  query {
    allBlogPosts {
      id
      title
      content
      published
      writer {
        username
      }
      likeSet {
        addedBy {
          username
        }
      }
      commentSet {
        addedBy {
          username
        }
        text
      }
    }
  }
  ```

- Get information about a specific blog post by ID:

  ```graphql
  query {
    blogPost(id: 1) {
      title
      content
      writer {
        username
      }
      likeSet {
        addedBy {
          username
        }
      }
      commentSet {
        addedBy {
          username
        }
        text
      }
    }
  }
  ```

- Create a blog post:

  ```graphql
  mutation {
    createBlogPost(title: "New Title", content: "New Content", writerData: { username: "seladb" }) {
      blogPost {
        id
        title
        published
      }
    }
  }
  ```

- Add "like" to an existing blog post:

  ```graphql
  mutation {
    addLike(blogId: 1, userData: { username: "seladb" }) {
      like {
        added
      }
    }
  }
  ```

- Add a comment to an existing blog post:

  ```graphql
  mutation {
    addComment(blogId: 1, userData: { username: "seladb" }, commentText: "NewComment") {
      comment {
        id
        added
      }
    }
  }  
  ```