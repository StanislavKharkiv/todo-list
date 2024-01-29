def routes(app):
    header = "<header><a href='/'>Root </a><a href='/home'>Home </a></header><hr>"
    style = "<style>a {font-size: 20px; margin: 10px;}</style>"

    @app.route("/")
    def index():
        return style + header + "<h1>Hello, World!</h1>"

    @app.route("/home")
    def home():
        return style + header + "<h1>home!</h1>"
