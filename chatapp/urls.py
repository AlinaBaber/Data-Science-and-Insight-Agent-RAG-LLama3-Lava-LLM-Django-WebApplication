from django.urls import path
from .import views
from .Conversation.views import create_conversation
from .messages.views import create_message
from .BotResponse.views import create_bot_response
from .UserPreference.views import create_user_preference
from .Analytics.views import create_analytics
from .KeywordIntent.views import create_keyword_intent
from .DatasetAndInputs.views import create_dataset_and_inputs

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path('accounts/login/', views.signin, name='login'),
    path("signout", views.signout, name="signout"),
    path("get-value", views.getValue),
    # path('update_current_conversation_id/', views.update_current_conversation_id, name='update_current_conversation_id'),
    path('upload/', views.upload_file, name='upload_file'),
    path("new_chat", views.newChat, name="new_chat"),
    path("end_chat", views.endChat, name="end_chat"),
    path('conversation/<int:conversation_id>/', views.fetch_conversation_data, name='fetch_conversation_data'),
    path('getConversationID', views.getConversationID, name='fetch_conversation_id'),
    path('create-conversation/', create_conversation, name='create_conversation'),
    path('create-message/', create_message, name='create_message'),
    path('create-bot-response/', create_bot_response, name='create_bot_response'),
    path('create-user-preference/', create_user_preference, name='create_user_preference'),
    path('create-analytics/', create_analytics, name='create_analytics'),
    path('create-keyword-intent/', create_keyword_intent, name='create_keyword_intent'),
    path('create_dataset_and_inputs/', create_dataset_and_inputs, name='create_dataset_and_inputs'),
    path('update-conversation-id', views.updateConversationID),
    path('get_column_names/', views.get_column_names, name='get_column_names'),
    path('get_selected_target_var', views.get_selected_target_var, name='get_selected_target_var'),
    path('get_date_column', views.get_date, name='get_date_column'),
    path('identify_problem_type/', views.identify_problem_type, name='identify_problem_type'),
    path('send_inputs_to_api', views.send_inputs_to_api, name='send_inputs_to_api'),
    path('get_process_logs', views.get_process_logs, name='get_process_logs'),
    path('get_input_json/', views.get_input_json, name='get_input_json')

]