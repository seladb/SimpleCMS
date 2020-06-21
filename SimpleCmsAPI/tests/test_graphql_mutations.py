
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from graphene_django.utils.testing import GraphQLTestCase
from SimpleCmsAPI.models import BlogPost, Like, Comment
from SimpleCMS.schema import schema


class GraphQLResponseException(Exception):
    def __init__(self, errorMsg):
        self.errorMsg = errorMsg


class MutationCreateBlogPostTest(GraphQLTestCase):

    GRAPHQL_SCHEMA = schema

    fixtures = ['test_db.json']

    def run_create_blog_mutation(self, title='New Title', content='New Content', username='seladb', expect_errors=False):

        response = self.query(
            '''
            mutation newBlogPost($title: String!, $content: String!, $username: String!) {
                createBlogPost(title: $title, content: $content, writerData: { username: $username}) {
                    blogPost {
                        title
                        id
                        content
                        published
                        writer {
                            username
                        }
                    }
                }
            }
            ''',
            op_name='newBlogPost',
            variables={
                'title': title,
                'content': content,
                'username': username,
            }
        )

        content = json.loads(response.content)
        
        if not expect_errors:
            self.assertResponseNoErrors(response)
        else:
            self.assertResponseHasErrors(response)
            raise GraphQLResponseException(content['errors'])

        self.assertIsNotNone(content['data'])

        return content['data']

    def test_create_blog_post(self):
        blog_post_count_start = BlogPost.objects.all().count()

        data = self.run_create_blog_mutation()

        newly_created_blog_post = data['createBlogPost']['blogPost']
        self.assertEqual(newly_created_blog_post['title'], 'New Title')
        self.assertEqual(newly_created_blog_post['content'], 'New Content')
        self.assertAlmostEqual(datetime.fromisoformat(newly_created_blog_post['published']), timezone.now(), delta=timezone.timedelta(seconds=3))
        blog_post_writer =  newly_created_blog_post['writer']
        self.assertEqual(blog_post_writer['username'], 'seladb')

        self.assertEqual(BlogPost.objects.all().count(), blog_post_count_start + 1)

    def test_create_blog_post_negative_tests(self):
        blog_post_count_start = BlogPost.objects.all().count()

        with self.assertRaises(GraphQLResponseException):
            self.run_create_blog_mutation(username='invalid_username', expect_errors=True)

        with self.assertRaises(GraphQLResponseException):
            self.run_create_blog_mutation(title='', expect_errors=True)

        with self.assertRaises(GraphQLResponseException):
            self.run_create_blog_mutation(content='', expect_errors=True)

        self.assertEqual(BlogPost.objects.all().count(), blog_post_count_start)


class MutationAddLikeTest(GraphQLTestCase):

    GRAPHQL_SCHEMA = schema

    fixtures = ['test_db.json']

    def run_add_like(self, blog_id=1, username='hereiam', expect_errors=False):
        response = self.query(
            '''
            mutation addLike($blogId: ID!, $username: String!) {
                addLike(blogId: $blogId, userData: { username: $username}) {
                    like {
                        addedBy {
                            username
                        }
                        blogPost {
                            id
                        }
                        added
                    }
                }
            }
            ''',
            op_name='addLike',
            variables={
                'blogId': blog_id,
                'username': username,
            }
        )

        content = json.loads(response.content)

        if not expect_errors:
            self.assertResponseNoErrors(response)
        else:
            self.assertResponseHasErrors(response)
            raise GraphQLResponseException(content['errors'])

        self.assertIsNotNone(content['data'])

        return content['data']['addLike']['like']
        
    def test_add_like(self):
        like_count_start = Like.objects.all().count()

        like_data = self.run_add_like()

        self.assertEqual(like_data['addedBy']['username'], 'hereiam')
        self.assertEqual(like_data['blogPost']['id'], 'QmxvZ1Bvc3ROb2RlOjE=')
        self.assertAlmostEqual(datetime.fromisoformat(like_data['added']), timezone.now(), delta=timezone.timedelta(seconds=3))

        self.assertEqual(Like.objects.all().count(), like_count_start + 1)

    def test_add_like_negative_tests(self):
        self.run_add_like(expect_errors=False)
        like_count_start = Like.objects.all().count()

        with self.assertRaises(GraphQLResponseException):
            with transaction.atomic():
                self.run_add_like(expect_errors=True)

        with self.assertRaises(GraphQLResponseException):
            self.run_add_like(blog_id=5, expect_errors=True)
        
        with self.assertRaises(GraphQLResponseException):
            self.run_add_like(username='invalid_username', expect_errors=True)

        self.assertEqual(Like.objects.all().count(), like_count_start)


class MutationAddCommentTest(GraphQLTestCase):

    GRAPHQL_SCHEMA = schema

    fixtures = ['test_db.json']

    def run_add_comment(self, blog_id=1, username='hereiam', comment_text='My Comment', expect_errors=False):
        response = self.query(
            '''
            mutation addComment($blogId: ID!, $username: String!, $commentText: String!) {
                addComment(blogId: $blogId, userData: { username: $username }, commentText: $commentText) {
                    comment {
                        addedBy {
                            username
                        }
                        blogPost {
                            id
                        }
                        added
                        text
                    }
                }
            }
            ''',
            op_name='addComment',
            variables={
                'blogId': blog_id,
                'username': username,
                'commentText': comment_text,
            }
        )

        content = json.loads(response.content)

        if not expect_errors:
            self.assertResponseNoErrors(response)
        else:
            self.assertResponseHasErrors(response)
            raise GraphQLResponseException(content['errors'])

        self.assertIsNotNone(content['data'])

        return content['data']['addComment']['comment']

    def test_add_comment(self):
        comment_count_start = Comment.objects.all().count()

        comment_data = self.run_add_comment()

        self.assertEqual(comment_data['addedBy']['username'], 'hereiam')
        self.assertEqual(comment_data['blogPost']['id'], 'QmxvZ1Bvc3ROb2RlOjE=')
        self.assertEqual(comment_data['text'], 'My Comment')
        self.assertAlmostEqual(datetime.fromisoformat(comment_data['added']), timezone.now(), delta=timezone.timedelta(seconds=3))

        self.assertEqual(Comment.objects.all().count(), comment_count_start + 1)

    def test_add_two_comments_by_same_user_to_same_blog_post(self):
        comment_count_start = Comment.objects.all().count()
        self.run_add_comment()
        self.run_add_comment()
        self.assertEqual(Comment.objects.all().count(), comment_count_start + 2)

    def test_add_comment_negative_tests(self):
        comment_count_start = Comment.objects.all().count()

        with self.assertRaises(GraphQLResponseException):
            self.run_add_comment(blog_id=5, expect_errors=True)

        with self.assertRaises(GraphQLResponseException):
            self.run_add_comment(username='invalid_username', expect_errors=True)

        with self.assertRaises(GraphQLResponseException):
            self.run_add_comment(comment_text='', expect_errors=True)

        self.assertEqual(Comment.objects.all().count(), comment_count_start)
