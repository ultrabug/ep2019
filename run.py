#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiohttp import web
from tartiflette import Engine
from tartiflette_aiohttp import register_graphql_handlers

import trello_to_graphql.resolvers

engine = Engine(
    [os.path.dirname(os.path.abspath(__file__)) + "/trello_to_graphql/sdl/queries.sdl"]
)
ctx = {}

web.run_app(
    register_graphql_handlers(
        app=web.Application(),
        engine=engine,
        executor_context=ctx,
        executor_http_endpoint="/graphql",
        executor_http_methods=["POST", "GET"],
        graphiql_enabled=True,
    )
)
