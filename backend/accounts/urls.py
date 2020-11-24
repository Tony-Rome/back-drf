from django.urls import path
from .views import WriterView, SessionView, WriterList, CollaboratorView, \
    CollaboratorListView, CommentView, CommentListView, DecisionView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts-urls'

urlpatterns = [
    path('custom/', WriterView.as_view()),
    path('session/', SessionView.as_view()),
    path('all-users/', WriterList.as_view()),
    path('collaborator/', CollaboratorView.as_view()),
    path('all-collaborators/', CollaboratorListView),
    path('comment-story/', CommentView.as_view()),
    path('all-comments/', CommentListView.as_view()),
    path('your-decision/', DecisionView.as_view()),
    #path('all-decision-by-type/')
]