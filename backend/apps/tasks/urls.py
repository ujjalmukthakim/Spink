from django.urls import path

from .views import AvailableTaskListView, ConfirmTaskView, MyTaskHistoryView

urlpatterns = [
    path("available/", AvailableTaskListView.as_view(), name="available-tasks"),
    path("history/", MyTaskHistoryView.as_view(), name="task-history"),
    path("confirm/", ConfirmTaskView.as_view(), name="task-confirm"),
]
