from django.db.models import QuerySet

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self) -> QuerySet:
        """Lấy tất cả các bản ghi."""
        return self.model.objects.all()

    def get_by_id(self, pk: int):
        """Lấy một bản ghi theo ID."""
        return self.model.objects.filter(pk=pk).first()

    def filter(self, **kwargs) -> QuerySet:
        """Lọc các bản ghi theo điều kiện."""
        return self.model.objects.filter(**kwargs)

    def create(self, **kwargs):
        """Tạo một bản ghi mới."""
        return self.model.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        """Cập nhật một bản ghi."""
        for field, value in kwargs.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, instance):
        """Xóa một bản ghi."""
        instance.delete()