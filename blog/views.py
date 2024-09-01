from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    """
    Выводит детальную страницу публикации блога
    """
    model = Blog

    def get_object(self, queryset=None):
        """
        Получает публикацию блога с увеличением счетчика просмотров
        """
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save(update_fields=['count_view'])
        return self.object
