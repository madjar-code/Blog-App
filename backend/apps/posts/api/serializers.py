from rest_framework.serializers import ModelSerializer
from users.api.serializers import UserSerializer

from posts.models import Post, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )
        # read_only_fields = ('__all__')


class PostSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'slug',
            'author',
            'thumbnail',
            'body',
            'read_time',
            'tags',
            'created_at',
        )
        read_only_fields = ('author',)