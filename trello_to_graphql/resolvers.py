from tartiflette import Resolver

from trello_to_graphql.managers import send_request


@Resolver("Query.member")
async def query_member(parent, args, ctx, info):
    # print("resolve member", parent, args)
    endpoint = "members/" + args.pop("id")
    return await send_request(endpoint, args)


@Resolver("Member.boards")
async def query_boards(parent, args, ctx, info):
    # print("resolve boards", parent, args)
    all_boards = []
    for idBoard in parent.get("idBoards", []):
        endpoint = "boards/" + idBoard
        all_boards.append(await send_request(endpoint, args))
    return all_boards


@Resolver("Member.organizations")
async def query_boards(parent, args, ctx, info):
    # print("resolve organizations", parent, args)
    all_orgs = []
    for idOrg in parent.get("idOrganizations", []):
        endpoint = "organizations/" + idOrg
        all_orgs.append(await send_request(endpoint, args))
    return all_orgs


@Resolver("Member.memberReferrer")
async def query_member_referrer(parent, args, ctx, info):
    # print("resolve member_referrer", parent, args)
    if parent.get("idMemberReferrer") is None:
        return
    endpoint = "members/" + parent.get("idMemberReferrer")
    return await send_request(endpoint, args)
