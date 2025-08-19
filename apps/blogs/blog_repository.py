from apps.common.base_repository import BaseRepository
from apps.blogs.models.blog_model import Blog

class BlogRepository(BaseRepository):
    def __init__(self):
        super().__init__(Blog)