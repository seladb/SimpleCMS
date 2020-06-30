# SimpleCMS

[![Django CI](https://github.com/seladb/SimpleCMS/workflows/Django%20CI/badge.svg)](https://github.com/seladb/SimpleCMS/actions?query=workflow%3A%22Django+CI%22)

This example project demonstrates the integration between Django and GraphQL.
It implements a very simple Content Management System (CMS) that allows creation of blog posts and adding likes and comments to them.

The project uses [Django](https://www.djangoproject.com/) and [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/) as Backend and [Gatsby](https://www.gatsbyjs.org) as a Frontend.

*NOTE: this example requires Python 3.7 or later and Node 12 or later*

## Installation

This project can be run locally or using [Docker Compose](https://docs.docker.com/compose/).

### Run locally

Clone the repo:

```shell
git clone https://github.com/seladb/SimpleCMS
```

#### Backend installation:

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

Alternatively you can load some demo data to your DB:

```shell
./load-demo-data.sh
```

*The password to `admin` is `admin` and the rest of the users is `simplecms`*

Run migrations and start server:

```shell
./run-backend-local.sh
```

Alternatively you can run migrations and start the server separately:

```shell
python manage.py migrate
```

```shell
python manage.py runserver
```

#### Frontend installation:

Install Gatsby:

```shell
npm install -g gatsby-cli
```

Install dependencies:

```shell
npm --prefix ./SimpleCMSWeb install ./SimpleCMSWeb
```

Make Sure Backend is up and then run:

```shell
./run-frontend-local.sh
```

Alternatively you can start Gatsby without the `run-frontend-local.sh` script:

```shell
cd SimpleCMSWeb
gatsby build
gatsby serve --port 8080
```

*NOTE: by default both Django and Gatsby are using port 8000, so to run both of them locally change Gatsby port to 8080*

### Run using Docker Compose

Make sure Docker and Docker Compose are installed.

Clone the repo:

```shell
git clone https://github.com/seladb/SimpleCMS
```

Run Docker Compose:

```shell
./run-docker.sh
```

This process will create docker images of PostgreSQL, Django backend and Gatsby frontend.

It will also load some demo data into the DB. 

*The password to `admin` is `admin` and the rest of the users is `simplecms`*

### Accessing the server and the frontend

Post installation the server should be available via this URL: <http://127.0.0.1:8000/>

There are currently two views available:

- Admin view: <http://127.0.0.1:8000/admin/>
- GraphiQL view: <http://127.0.0.1:8000/graphql/>

The Gatsby frontend is available via this URL: <http://127.0.0.1:8080>

### Run tests

To run the unit-tests execute the following command:

```shell
python manage.py test
```

## GraphQL queries and mutations

Below are the GraphQL queries and mutations currently available. [GraphiQL](http://127.0.0.1:8000/graphql/) can be used to test them. Before running queries please make sure to create users via [Django Admin interface](http://127.0.0.1:8000/admin/)

- Fetch blog posts from the database with optional filtering by blog post ID, blog post writer, and blog post title:

  ```graphql
  query allBlogPostsQuery($id: ID, $writer_Username: String, $title_Contains: String, $title: String) {
    allBlogPosts(id: $id, writer_Username: $writer_Username, title_Contains: $title_Contains, title: $title) {
      edges {
        node {
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