from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.OpportunityListView.as_view(), name='list'),
    path('kanban/', views.OpportunityKanbanView.as_view(), name='kanban'),
    path('create/', views.OpportunityCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.OpportunityDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.OpportunityUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/move/', views.OpportunityMoveStageView.as_view(), name='move'),
    path('<uuid:pk>/convert/', views.OpportunityConvertToProjectView.as_view(), name='convert'),
]