from django.urls import include, path

from classification.views import DogBreedDectectionView

classification_urlpatterns = [path("dog-breeds", DogBreedDectectionView.as_view())]

urlpatterns = [path("classification/", include(classification_urlpatterns))]
