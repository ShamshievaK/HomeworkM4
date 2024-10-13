"""
URL configuration for HW4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts.views import test_view, main_page_view, post_list_view, post_detail_view

urlpatterns = [                                # ссылка-путеводитель по сайту
    path('admin/', admin.site.urls),
    path('test/', test_view),
    path("", main_page_view),
    path("posts/", post_list_view),
    path("posts/<int:post_id>/", post_detail_view)
]
