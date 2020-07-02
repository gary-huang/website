import graphene

from graphene_django.types import DjangoObjectType

from church import models


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name"]


class Query(graphene.ObjectType):
    current_user = graphene.Field(UserType)

    def resolve_current_user(self, info, **kwargs):
        return models.User.objects.first()


schema = graphene.Schema(query=Query)
