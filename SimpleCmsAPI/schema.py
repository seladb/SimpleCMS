import graphene
from graphene_django.types import DjangoObjectType
from .models import BlogPost, User, Comment, Like

class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost

class UserType(DjangoObjectType):
    class Meta:
        model = User

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class Query(object):
    all_blog_posts = graphene.List(BlogPostType)

    blog_post = graphene.Field(BlogPostType, id=graphene.ID())

    def resolve_all_blog_posts(self, info, **kwargs):
        return BlogPost.objects.all()

    def resolve_blog_post(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return BlogPost.objects.get(pk=id)


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    id = graphene.ID()


def get_user_object(user_data):
    if user_data.username is not None:
        return User.objects.get(username=user_data.username)
    elif user_data.id is not None:
        return User.objects.get(id=user_data.id)


class CreateBlogPost(graphene.Mutation):
    class Arguments:
        title = graphene.NonNull(graphene.String)
        content = graphene.NonNull(graphene.String)
        writer_data = graphene.NonNull(UserInput)

    blog_post = graphene.Field(BlogPostType)
    
    @staticmethod
    def mutate(root, info, title, content, writer_data):
        blog_post = BlogPost(
            title=title,
            content=content,
            writer=get_user_object(writer_data)
        )
        blog_post.save()

        return CreateBlogPost(blog_post=blog_post)


class AddLike(graphene.Mutation):
    class Arguments:
        blog_id = graphene.NonNull(graphene.ID)
        user_data = graphene.NonNull(UserInput)

    like = graphene.Field(LikeType)
    
    @staticmethod
    def mutate(root, info, blog_id, user_data):
        brand_new_like = Like(
            added_by=get_user_object(user_data),
            blog_post=BlogPost.objects.get(id=blog_id)
        )
        brand_new_like.save()
        return AddLike(like=brand_new_like)


class AddComment(graphene.Mutation):
    class Arguments:
        blog_id = graphene.NonNull(graphene.ID)
        user_data = graphene.NonNull(UserInput)
        comment_text = graphene.NonNull(graphene.String)

    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(root, info, blog_id, user_data, comment_text):
        brand_new_comment = Comment(
            added_by=get_user_object(user_data),
            blog_post=BlogPost.objects.get(id=blog_id),
            text=comment_text
        )
        brand_new_comment.save()

        return AddComment(comment=brand_new_comment)


class Mutation(graphene.ObjectType):
    create_blog_post = CreateBlogPost.Field()
    add_like = AddLike.Field()
    add_comment = AddComment.Field()
