from apps.{appname}.handlers.v0 import main


routes = [

    (r'^/example$',
        main.ExampleHandler),
]
