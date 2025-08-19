from apps.blogs.blog_repository import BlogRepository
from apps.common.base_service import BaseService

class BlogService(BaseService):
    def __init__(self):
        super().__init__(BlogRepository())