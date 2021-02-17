import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from church import models


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name"]


class AuthMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
        token = graphene.String()

    def mutate(self, info, username, password, token):
        print(username, password, token)
        return AuthMutation()


class ServicePageNode(DjangoObjectType):
    class Meta:
        model = models.ServicePage
        only_fields = ["id", "title", "slug", "description", "date"]
        filter_fields = ["id", "title", "slug"]
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    current_user = graphene.Field(UserType)
    # services = graphene.List(ServiceNode)
    service = relay.Node.Field(ServicePageNode)
    services = DjangoFilterConnectionField(ServicePageNode)

    def resolve_current_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        else:
            return None

    # @graphene.resolve_only_args
    # def resolve_services(self):
    #     return models.ServicePage.objects.live()


schema = graphene.Schema(query=Query)
