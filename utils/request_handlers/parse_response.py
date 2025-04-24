class DiscordEmbedAuthor:
    def __init__(self, name: str, icon_url: str | None = None, url: str | None = None) -> None:
        self.name = name
        self.icon_url = icon_url
        self.url = url

    name: str
    icon_url: str | None = None
    url: str | None = None

class DiscordEmbedField:
    def __init__(self, name: str, value: str, inline: bool = False) -> None:
        self.name = name
        self.value = value
        self.inline = inline

    name: str
    value: str
    inline: bool = False

class DiscordEmbedData:
    def __init__(self, title: str, thumbnailImage: str | None = None, author: DiscordEmbedAuthor | None = None, description: str | None = None, fields: list[DiscordEmbedField] | None = None) -> None:
        self.title = title
        self.thumbnailImage = thumbnailImage
        self.author = author
        self.description = description
        self.fields = fields
        
    title: str
    thumbnailImage: str | None = None
    author: DiscordEmbedAuthor | None = None
    description: str | None = None
    fields: list[DiscordEmbedField] | None = None
