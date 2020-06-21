import json
from datetime import datetime, timedelta
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase
from SimpleCMS.schema import schema


class QueryTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    fixtures = ['test_db.json']

    def run_all_blog_posts_query(self, blog_id=None, writer_username=None, title=None, title_contains=None):
        response = self.query(
            '''
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
            ''',

            op_name='allBlogPostsQuery',
            variables={
                'id': blog_id,
                'writer_Username': writer_username,
                'title': title,
                'title_Contains': title_contains,
            }
        )

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.content)

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        return content

    def test_all_blog_posts_query(self):
        content = self.run_all_blog_posts_query()

        self.assertEquals(len(content['data']['allBlogPosts']['edges']), 2)

        blog_post1 = content['data']['allBlogPosts']['edges'][0]['node']
        self.assertEquals(blog_post1['title'], 'PcapPlusPlus reached 1000 GitHub stars')
        self.assertEquals(len(blog_post1['likeSet']), 2)
        blog_post1_like = blog_post1['likeSet'][1]
        self.assertEquals(blog_post1_like['addedBy']['username'], 'omg')
        self.assertEquals(len(blog_post1['commentSet']), 1)
        blog_post1_comment = blog_post1['commentSet'][0]
        self.assertEquals(blog_post1_comment['text'], 'Way to go!')
        writer_blog_post1 = blog_post1['writer']
        self.assertEquals(writer_blog_post1['username'], 'seladb')

        blog_post2 = content['data']['allBlogPosts']['edges'][1]['node']
        self.assertEquals(blog_post2['title'], 'PcapPlusPlus README file')
        self.assertEquals(len(blog_post2['likeSet']), 3)
        blog_post2_like = blog_post2['likeSet'][0]
        self.assertEquals(blog_post2_like['addedBy']['username'], 'omg')
        self.assertEquals(len(blog_post2['commentSet']), 2)
        blog_post2_comment = blog_post2['commentSet'][0]
        self.assertEquals(blog_post2_comment['text'], 'Wow!!')
        writer_blog_post2 = blog_post2['writer']
        self.assertEquals(writer_blog_post2['username'], 'cooluser')

    def test_blog_post_query_filter_by_id(self):
        content = self.run_all_blog_posts_query(blog_id="QmxvZ1Bvc3ROb2RlOjE=")

        self.assertEquals(len(content['data']['allBlogPosts']['edges']), 1)
        blog_post = content['data']['allBlogPosts']['edges'][0]['node']
        self.assertEqual(blog_post['title'], 'PcapPlusPlus reached 1000 GitHub stars')
        self.assertIn('1000 GitHub stars!!', blog_post['content'])
        self.assertAlmostEqual(datetime.fromisoformat(blog_post['published']), datetime(2020, 6, 18, 8, 49, 31, tzinfo=timezone.utc), delta=timedelta(seconds=1))
        blog_post_writer = blog_post['writer']
        self.assertEqual(blog_post_writer['username'], 'seladb')

    def test_blog_post_query_filter_by_writer(self):
        content = self.run_all_blog_posts_query(blog_id="seladb")

        self.assertEquals(len(content['data']['allBlogPosts']['edges']), 2)

    def test_blog_post_query_filter_by_title_contains(self):
        content = self.run_all_blog_posts_query(title_contains="1000")

        self.assertEquals(len(content['data']['allBlogPosts']['edges']), 1)
        blog_post = content['data']['allBlogPosts']['edges'][0]['node']
        self.assertIn('1000', blog_post['title'])


