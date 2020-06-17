from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from SimpleCmsAPI.models import User, BlogPost, Like, Comment

def create_user(username='seladb', first_name='Elad', last_name='B'):
    new_user = User(username=username, first_name=first_name, last_name=last_name)
    new_user.save()
    return new_user

def create_blog_post(writer, title='New Post', content='Blah Blah Blah...'):
    new_blog_post = BlogPost(title=title, content=content, writer=writer)
    new_blog_post.save()
    return new_blog_post


class UserModelTests(TestCase):

    def test_simple_user_create_retrieve(self):
        create_user()
        self.assertEqual(User.objects.all().count(), 1)

        create_user(username='seladb2')
        self.assertEqual(User.objects.all().count(), 2)

        user1 = User.objects.get(id=1)
        self.assertEqual(user1.username, 'seladb')
        self.assertEqual(user1.first_name, 'Elad')

    def test_user_to_string(self):
        create_user()
        self.assertEquals(str(User.objects.get(pk=1)), 'Elad B')

    def test_create_blank_user(self):
        with self.assertRaises(ValidationError):
            User().full_clean()

    def test_create_two_users_with_same_username(self):
        create_user()
        self.assertEqual(User.objects.all().count(), 1)
        with self.assertRaises(IntegrityError):
            create_user()


class BlogPostModelTests(TestCase):

    def setUp(self):
        self.user = create_user()

    def test_blog_post_create_and_retreive(self):
        create_blog_post(self.user)
        self.assertEquals(BlogPost.objects.all().count(), 1)

        blog_post = BlogPost.objects.get(pk=1)
        self.assertIsNotNone(blog_post)
        self.assertEquals(blog_post.title, 'New Post')

        with self.assertRaises(BlogPost.DoesNotExist):
            BlogPost.objects.get(pk=2)

    def test_blog_post_to_string(self):
        blog_post_with_short_title = create_blog_post(writer=self.user, title='Short Title')
        self.assertEquals(str(blog_post_with_short_title), blog_post_with_short_title.title)

        blog_post_with_long_title = create_blog_post(writer=self.user, title='Very Very Very Very Very Very Very Very Long Title')
        self.assertEquals(str(blog_post_with_long_title), blog_post_with_long_title.title[:40] + '...')

        blog_post_with_43_chars_title = create_blog_post(writer=self.user, title='Very Very Very VeryVery VeryVery Long Title')
        self.assertEquals(str(blog_post_with_43_chars_title), blog_post_with_43_chars_title.title)

    def test_blog_post_empty_fields(self):
        with self.assertRaises(ValidationError):
            create_blog_post(self.user, title='').full_clean()

        with self.assertRaises(ValidationError):
            create_blog_post(self.user, content='').full_clean()

        with self.assertRaises(IntegrityError):
            create_blog_post(writer=None)


class LikeAndCommentTests(TestCase):

    def create_user_and_blogpost_fixture(self):
        user_seladb = create_user()
        return user_seladb, create_blog_post(writer=user_seladb)

    def test_create_blog_and_add_comments_and_likes(self):
        user_seladb = create_user()
        user_cooluser = create_user(username='cooluser', first_name='Cool', last_name='User')
        user_helloworld = create_user(username='helloworld', first_name='Hello', last_name='World')

        blog_seldab1 = create_blog_post(writer=user_seladb)
        blog_seldab2 = create_blog_post(writer=user_seladb, title='New Post 2')
        blog_cooluser = create_blog_post(writer=user_cooluser, title='Cool Blog Post', content='Bli Bli Bli')

        self.assertEquals(User.objects.all().count(), 3)
        self.assertEquals(BlogPost.objects.all().count(), 3)

        Like(blog_post=blog_seldab1, added_by=user_cooluser).save()
        Like(blog_post=blog_seldab2, added_by=user_cooluser).save()
        Like(blog_post=blog_seldab2, added_by=user_seladb).save()
        Like(blog_post=blog_cooluser, added_by=user_helloworld).save()
        Like(blog_post=blog_cooluser, added_by=user_seladb).save()

        self.assertEquals(Like.objects.all().count(), 5)
        self.assertEquals(Like.objects.filter(blog_post__writer__username='seladb').count(), 3)
        self.assertEquals(Like.objects.filter(blog_post__writer__username='cooluser').count(), 2)
        self.assertEquals(Like.objects.filter(blog_post__title__contains='Cool').count(), 2)

        Comment(blog_post=blog_seldab1, added_by=user_cooluser, text='Very interesting').save()
        Comment(blog_post=blog_seldab1, added_by=user_helloworld, text='Hello world').save()
        Comment(blog_post=blog_seldab2, added_by=user_seladb, text='Please comment').save()
        Comment(blog_post=blog_cooluser, added_by=user_helloworld, text='Hello nice post').save()
        Comment(blog_post=blog_cooluser, added_by=user_seladb, text='Posty post').save()

        self.assertEquals(Comment.objects.all().count(), 5)
        self.assertEquals(Comment.objects.filter(blog_post__writer__username='seladb').count(), 3)
        self.assertEquals(Comment.objects.filter(blog_post__writer__username='cooluser').count(), 2)
        self.assertEquals(Comment.objects.filter(text__contains='Hello').count(), 2)

    def test_invalid_like(self):
        (user_seladb, blog_post_seladb) = self.create_user_and_blogpost_fixture()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Like(blog_post=blog_post_seladb).save()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Like(added_by=user_seladb).save()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Like().save()

    def test_invalid_comment(self):
        (user_seladb, blog_post_seladb) = self.create_user_and_blogpost_fixture()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Comment(blog_post=blog_post_seladb).save()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Comment(added_by=user_seladb).save()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Comment().save()

        with self.assertRaises(ValidationError):
            Comment(blog_post=blog_post_seladb, added_by=user_seladb).full_clean()

    def test_invalid_two_likes_from_same_user_to_same_blog_post(self):
        (user_seladb, blog_post_seladb) = self.create_user_and_blogpost_fixture()
        Like(added_by=user_seladb, blog_post=blog_post_seladb).save()

        with self.assertRaises(IntegrityError):
            Like(added_by=user_seladb, blog_post=blog_post_seladb).save()

    def test_valid_two_comments_from_same_user_to_same_blog_post(self):
        (user_seladb, blog_post_seladb) = self.create_user_and_blogpost_fixture()
        Comment(added_by=user_seladb, blog_post=blog_post_seladb, text='Hello').save()
        Comment(added_by=user_seladb, blog_post=blog_post_seladb, text='Hello').save()