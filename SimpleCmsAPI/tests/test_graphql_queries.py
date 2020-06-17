import json
from datetime import datetime, timedelta
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase
from SimpleCMS.schema import schema

class QueryTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    fixtures = ['test_db.json']

    def test_all_blog_posts_query(self):

        response = self.query(
            '''
            query {
                allBlogPosts {
                    id
                    title
                    writer {
                        username
                        firstName
                        lastName
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
            '''
        )

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.content)

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertIsNotNone(content['data'])
        self.assertIsNotNone(content['data']['allBlogPosts'])
        self.assertEquals(len(content['data']['allBlogPosts']), 2)

        blog_post1 = content['data']['allBlogPosts'][0]
        self.assertEquals(blog_post1['title'], 'PcapPlusPlus reached 1000 GitHub stars')
        self.assertEquals(len(blog_post1['likeSet']), 3)
        blog_post1_like = blog_post1['likeSet'][2]
        self.assertEquals(blog_post1_like['addedBy']['username'], 'omg')
        self.assertEquals(len(blog_post1['commentSet']), 3)
        blog_post1_comment = blog_post1['commentSet'][1]
        self.assertEquals(blog_post1_comment['text'], 'To the next 1000!!!')
        writer_blog_post1 = blog_post1['writer']
        self.assertEquals(writer_blog_post1['username'], 'seladb')
        self.assertEquals(writer_blog_post1['firstName'], 'Elad')

        blog_post2 = content['data']['allBlogPosts'][1]
        self.assertEquals(blog_post2['title'], 'Scaling Your Analytics Schema Using Events Grammar')
        self.assertEquals(len(blog_post2['likeSet']), 2)
        blog_post2_like = blog_post2['likeSet'][0]
        self.assertEquals(blog_post2_like['addedBy']['username'], 'seladb')
        self.assertEquals(len(blog_post2['commentSet']), 1)
        blog_post2_comment = blog_post2['commentSet'][0]
        self.assertEquals(blog_post2_comment['text'], 'Nice post!')
        writer_blog_post2 = blog_post2['writer']
        self.assertEquals(writer_blog_post2['username'], 'cooluser')
        self.assertEquals(writer_blog_post2['lastName'], 'User')

    def test_blog_post_query(self):

        response = self.query(
            '''
            query blogPostQuery($id: ID!) {
                blogPost(id: $id) {
                    published
                    title
                    content
                    writer {
                        username
                    }
                }
            }
            ''',
            variables={ 'id': '1' }
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertIsNotNone(content['data'])
        
        blog_post = content['data']['blogPost']
        self.assertEqual(blog_post['title'], 'PcapPlusPlus reached 1000 GitHub stars')
        self.assertIn('1000 GitHub stars!!', blog_post['content'])
        self.assertAlmostEqual(datetime.fromisoformat(blog_post['published']), datetime(2020, 6, 15, 21, 16, 4, tzinfo=timezone.utc), delta=timedelta(seconds=1))
        blog_post_writer = blog_post['writer']
        self.assertEqual(blog_post_writer['username'], 'seladb')


class MutationTest(GraphQLTestCase):

    GRAPHQL_SCHEMA = schema

    fixtures = ['test_db.json']

    def run_create_blog_mutation(self, title='New Title', content='New Content', username='seladb', assertCorrectResponse=True):
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
        
        if assertCorrectResponse:
            self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertIsNotNone(content['data'])

        return content['data']

    def test_create_blog_post(self):

        data = self.run_create_blog_mutation()

        newly_created_blog_post = data['createBlogPost']['blogPost']
        self.assertEqual(newly_created_blog_post['title'], 'New Title')
        self.assertEqual(newly_created_blog_post['content'], 'New Content')
        self.assertAlmostEqual(datetime.fromisoformat(newly_created_blog_post['published']), timezone.now(), delta=timezone.timedelta(seconds=3))
        blog_post_writer =  newly_created_blog_post['writer']
        self.assertEqual(blog_post_writer['username'], 'seladb')


    # def test_create_blog_post_invalid_username(self):
    #     try:
    #         data = self.run_create_blog_mutation(username='asddsfs', assertCorrectResponse=False)
    #     except Exception as e:
    #         print(type(e))