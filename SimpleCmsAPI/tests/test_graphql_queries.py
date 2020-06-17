import json
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
