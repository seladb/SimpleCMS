import graphene

import SimpleCmsAPI.schema


class Query(SimpleCmsAPI.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=SimpleCmsAPI.schema.Mutation)