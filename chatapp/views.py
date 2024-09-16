from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .Conversation.models import Conversation
from .messages.models import Message
from .BotResponse.models import BotResponse
from .DatasetAndInputs.models import DatasetandInput
from .bot.models import Bot
# import openai
import json
import logging
from django.utils import timezone
import pytz
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import pandas as pd
from textblob import TextBlob
from django.core.serializers import serialize
import requests
from django.http import JsonResponse
from langdetect import detect
from django.http import JsonResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
import os
import ast
import re
# Initialize logging
logger = logging.getLogger(__name__)

import re
bot = None  # Initialize bot as None


try:
    bot = Bot.objects.get(bot_name="Insight_agent")  # Attempt to get the existing bot
except Bot.DoesNotExist:
    bot = Bot.objects.create(  # Create a new bot if it doesn't exist
        bot_name="Insight_agent",
        status="active",
        description="a bot"
    )

cons = None

@login_required
def index(request):

    try:
        # today = timezone.now()
        # yesterday = today - timedelta(days=1)
        # seven_days_ago = today - timedelta(days=7)

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        seven_days_ago = today - timedelta(days=7)

        cons = Conversation.objects.filter(users=request.user)

        print("Conversations: ", cons)

        t_conversations = cons.filter(end_time__gte=today, end_time__lt=today + timedelta(days=1))
        print("today's conversation", t_conversations)

        y_conversations = cons.filter(end_time__gte=yesterday, end_time__lt=yesterday + timedelta(days=1))
        print("yesterday conversation: ", y_conversations)

        s_conversations = cons.filter(end_time__gte=seven_days_ago, end_time__lt=today)
        print("week ago conversation: ", s_conversations)

        cons = Conversation.objects.filter(users=request.user).order_by('-end_time')
        t_conversations = t_conversations.order_by('-end_time')
        y_conversations = y_conversations.order_by('-end_time')
        s_conversations = s_conversations.order_by('-end_time')
        print('cons after ordering: ', cons)

        # t_conversations = cons.filter(end_time__date=today)
        # print("today's conversation", t_conversations)
        # y_conversations = cons.filter(end_time__date=yesterday)
        # print("yesterday conversation: ", y_conversations)
        # s_conversations = cons.filter(end_time__date=seven_days_ago)
        # print("week ago conversation: ", s_conversations)
        #
        # cons = Conversation.objects.filter(users=request.user).order_by('-end_time')
        # t_conversations = t_conversations.order_by('-end_time')
        # y_conversations = y_conversations.order_by('-end_time')
        # s_conversations = s_conversations.order_by('-end_time')

        context = {
            "t_conversations": t_conversations,
            "y_conversations": y_conversations,
            "s_conversations": s_conversations,
            "all_conversations": cons
        }
    except Exception as e:
        logger.error(f"Error fetching conversation data: {e}")
        context = {
            "error_message": "An error occurred while fetching conversation data. Please try again later."
        }

    return render(request, "chatapp/index.html", context)



def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    context = {"form": form}
    return render(request, "chatapp/signup.html", context)


def signin(request):
    err = None
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")

        else:
            err = "Invalid Credentials"


    context = {"error": err}
    return render(request, "chatapp/signin.html", context)


def signout(request):
    logout(request)
    context = {}
    return render(request, "chatapp/signin.html", context)


import requests


def autocorrect_text(text):
    try:
        # Detect the language of the text
        if detect(text) == 'en':
            blob = TextBlob(text)
            corrected_text = blob.correct()
            return str(corrected_text)
        else:
            return text
    except Exception as e:
        return f"An error occurred: {e}"



def answer_query(message, process_id=None):
    api_url = 'http://10.0.0.83:8000/chatwith-agent/'
    headers = {'Content-Type': 'application/json'}

    try:

        corrected_text = autocorrect_text(message)
        print('corrected message: ', corrected_text)
        message = str(corrected_text)
        # Sending the request data as JSON
        response = requests.post(api_url, json={'query': message, 'process_id': process_id}, headers=headers)

        # Check if the response was successful
        if response.ok:
            response_data = response.json()  # This might raise a ValueError if not JSON
            print("Full response_data: ", response_data)

            # Check if 'response' key is in the response_data
            if 'response' in response_data:
                botResult = response_data['response']
                print("Extracted Result:", botResult)

                return botResult
            else:
                print("Error: 'response' key missing in JSON response")
        else:
            print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
    except Exception as e:
        # General error handling
        print(f"An error occurred: {str(e)}")

    return None


def tokenize(text):
    # Using regex to split by non-alphanumeric characters
    return re.findall(r'\w+', text.lower())


def check_message_for_fn_list(message, fn_list):
    print('checking for message fn_list..')
    message_tokens = tokenize(message)
    print('message_tokens: ', message_tokens)

    for phrase in fn_list:
        phrase_tokens = tokenize(phrase)
        print('phrase_tokens: ', phrase_tokens)
        if set(phrase_tokens).intersection(message_tokens):
            print('intersection')
            return True

    return False


def trigger_modal(columns):
    print(columns)


@login_required
def getValue(request):
    try:

        # request.session['predict_flag'] = False

        data = json.loads(request.body)
        user_message = data["msg"]

        conversation_id = request.session.get('conversation_id')
        print('session conversation_id: ', conversation_id)
        conversation = Conversation.objects.get(id=conversation_id)

        print('user message: ', user_message)

        data_input = DatasetandInput.objects.filter(conversation_id=conversation_id).first()
        if data_input:
            print("conversation_id: ", data_input.conversation_id)

            print('input columns type: ', type(data_input.inputcolumns))
            print('input columns: ', data_input.inputcolumns)

            problem_type = data_input.problem_type
            target_variable = data_input.target_variable
            inputcolumns = eval(data_input.inputcolumns)

            print('problem type: ', problem_type)
            print('target var: ', target_variable)
            print('input columns: ', type(inputcolumns))
            print('input columns: ', inputcolumns)

            if request.session.get('predict_flag') is False or not request.session.get('predict_flag'):

                fn_list = []

                if problem_type == 'categorical' or problem_type == 'numerical':
                    if problem_type == 'categorical':
                        print('categorical')
                        fn_list = ['inference_predict_classify_from_classification model', ' type', 'classify', 'categorize', 'give class', 'give type', 'give class']

                        if check_message_for_fn_list(user_message, fn_list):
                            request.session['last_query'] = user_message
                            request.session['predict_flag'] = True
                            return JsonResponse({"msg": user_message, "columns": inputcolumns})
                    else:
                        fn_list = ['predict', 'inference_predict_from regression model', ' value', 'predict', 'give prediction']

                        print('numerical')

                        if check_message_for_fn_list(user_message, fn_list):
                            request.session['last_query'] = user_message
                            request.session['predict_flag'] = True
                            return JsonResponse({"msg": user_message, "columns": inputcolumns})

        # if request.session.get('predict_flag'):


        # Properly access inputs from session
        inputs = request.session.get('json_input', {})

        if inputs:
            user_message += ' ' + ' '.join(f"{k}:{v}" for k, v in inputs.items())
            print('user_message: ', user_message)
            request.session['json_input']=''

        print('user_message:', user_message)

        if conversation.title == '' or not conversation.title or conversation.title == 'null' or conversation.title is None:
            conversation.title = user_message
            conversation.save()

        if conversation.process_id:
            response = answer_query(user_message, conversation.process_id)
        else:
            response = answer_query(user_message, None)

        # Convert current UTC time to Pakistan Standard Time
        pkt_timezone = pytz.timezone('Asia/Karachi')
        pkt_time_now = timezone.now().astimezone(pkt_timezone)

        print("user_message: ", user_message)
        print('response: ', response)


        conversation = Conversation.objects.filter(users=request.user, id=conversation_id).first()
        print(f"type conv: {type(conversation)}")
        print(f"session conversation: {conversation}")

        if not conversation:
            c = Conversation.objects.create(
                start_time=pkt_time_now,  # Record start time in PKT
                end_time=pkt_time_now,    # Record end time in PKT
                users=request.user,
                bot=bot,
                status="open"
            )
            conversation = c
            conversation_id = conversation.id

            print('conversation_id: ', conversation_id)
            print(f"conversation: {conversation}")

            request.session['conversation_id'] = conversation_id

        # Record message time in PKT
        message = Message.objects.create(
            message=user_message,
            sent_at=pkt_time_now,
            conversation=conversation,
            sender=request.user
        )

        bot_response = BotResponse.objects.create(
            response_text=response,
            created_at=pkt_time_now,
            message=message
        )

        conversation.end_time = pkt_time_now
        if conversation.title == '' or not conversation.title:
            conversation.title = user_message
        conversation.save()

        return JsonResponse({"msg": user_message, "res": response, "conv": conversation.id})
    except Exception as e:
        logger.error(f"Error processing user input: {e}")
        return JsonResponse({"error_message": "An error occurred while processing your request. Please try again later."})

def get_input_json(request):
    print('inside get input json')
    data = json.loads(request.body)
    inputs = data['columns']
    print('inputs: ', inputs)
    request.session['json_input'] = inputs

    return JsonResponse({'message': 'Saved input JSON to session storage!'})

def newChat(request):
    conversation = Conversation.objects.create(
        start_time=timezone.now(),
        end_time=timezone.now(),
        users=request.user,
        bot=bot,
        status="open"
    )

    request.session['conversation_id'] = conversation.id
    context = {"conversation_id": conversation.id}
    print(context)
    return JsonResponse(context)


def endChat(request):
    print("request con id", request.conversation_id)


def fetch_conversation_data(request, conversation_id):
    try:
        # Assuming Message and BotResponse models have fields like 'conversation_id' and 'message_id'
        print(conversation_id)
        messages = Message.objects.filter(conversation_id=conversation_id).order_by('sent_at')

        print(messages)
        messages_data = [{'id': message.id, 'text': message.message} for message in messages]

        bot_responses = []
        for message in messages:
            responses = BotResponse.objects.filter(message_id=message.id)
            print(responses)
            responses_data = [{'id': response.id, 'response_text': response.response_text, 'message_id': response.message_id} for response in responses]
            bot_responses.append(responses_data)

        return JsonResponse({'messages': messages_data, 'bot_responses': bot_responses})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



# Add this view to handle updating the current conversation ID
# def update_current_conversation_id(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         conversation_id = data.get('conversation_id')
#         if conversation_id is not None:
#             # Update the current conversation ID in session, database, or any other suitable storage mechanism
#             request.session['current_conversation_id'] = conversation_id
#             return JsonResponse({'success': True})
#
#     return JsonResponse({'success': False}, status=400)


def updateConversationID(request):
    try:
        data = json.loads(request.body)
        conversation_id = data["conversation_id"]

        print("conversation_id: ", conversation_id)

        request.session['conversation_id'] = conversation_id

        return JsonResponse({"conversation_id": conversation_id})
    except Exception as e:
        logger.error(f"Error processing user input: {e}")
        return JsonResponse({"error_message": "An error occurred while processing your request. Please try again later."})


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()

        # Check if the file has allowed extensions
        allowed_extensions = ['.csv', '.xls', '.xlsx', '.pdf', '.docx', '.txt', '.jpg','.jpeg','.png']
        if file_ext not in allowed_extensions:
            return JsonResponse({'error': 'Unsupported file type.'}, status=400)

        # Save the file using Django's FileSystemStorage
        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'datasets'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Determine the problem type based on file extension
        if file_ext in ['.docx', '.pdf', '.txt']:
            problem_type = 'DocumentAnalysis'
        elif file_ext in ['.jpg','.jpeg','.png']:
            problem_type = 'ImageAnalysis'
        else:
            problem_type =None

        # Retrieve conversation based on session
        conversation_id = request.session.get('conversation_id')
        conversation = Conversation.objects.filter(id=conversation_id, users=request.user).first()

        # Create DatasetandInput entry
        try:
            data_input = DatasetandInput.objects.create(
                conversation=conversation,
                file=uploaded_file,
                problem_type=problem_type
            )
        except Exception as e:
            return JsonResponse({'error': 'Failed to save file information.'}, status=500)

        # Return successful response
        return JsonResponse(
            {'message': 'File uploaded successfully', 'problem_type': problem_type, 'file_url': file_url}, status=200)

    # Handle case where no file is provided
    return JsonResponse({'error': 'No file uploaded'}, status=400)


def getConversationID(request):
    conversation_id = request.session.get('conversation_id')
    return JsonResponse({'conversation_id': conversation_id})



def get_column_names(request):
    # file_path = 'UserUploadedFiles/Diabetes.csv'

    conversation_id = request.session.get('conversation_id')
    print('session conversation_id: ', conversation_id)

    conversation = Conversation.objects.filter(users=request.user, id=conversation_id).first()

    data_input = DatasetandInput.objects.filter(conversation_id=conversation.id).first()

    file_path = data_input.file

    df = pd.read_csv(file_path)
    column_names = df.columns.tolist()

    # return render(request, 'chatapp/index.html', {'column_names': column_names})
    return JsonResponse({'column_names': column_names})


def get_selected_target_var(request):

    data = json.loads(request.body)
    target_var = data['target_var']

    print("Target var: ", target_var)

    conversation_id = request.session.get('conversation_id')
    print('session conversation_id: ', conversation_id)

    conversation = Conversation.objects.filter(users=request.user, id=conversation_id).first()

    data_input = DatasetandInput.objects.filter(conversation_id = conversation.id).first()

    file_path = data_input.file
    # file_path = 'UserUploadedFiles/Diabetes.csv'

    data = pd.read_csv(file_path)

    isNumeric = False
    date_cols = []

    if pd.api.types.is_numeric_dtype(data[target_var]):
        isNumeric = True
        date_cols = get_date_columns(data)
        # type, second_type, columns, date_cols = analyze_problem_type(data, target_var)

    conversation_id = request.session.get('conversation_id')
    print('session conversation_id: ', conversation_id)

    # conversation = Conversation.objects.filter(users=request.user, id=conversation_id).first()

    data_input = DatasetandInput.objects.filter(conversation_id=conversation_id).first()

    data_input.target_variable = target_var
    data_input.save()

    return JsonResponse({'isNumeric': isNumeric, 'date_columns': date_cols})



def get_date_columns(dataframe):
    date_columns = []

    for column in dataframe.columns:
        if pd.api.types.is_datetime64_any_dtype(dataframe[column]):
            date_columns.append(column)
        elif pd.api.types.is_object_dtype(dataframe[column]):
            try:
                pd.to_datetime(dataframe[column])
                date_columns.append(column)
            except ValueError:
                pass

    date_columns.append(None)
    return date_columns


def get_date(request):
    data = json.loads(request.body)
    date_column = data['date_column']
    print('date_column: ', date_column)

    conversation_id = request.session.get('conversation_id')
    print('session conversation_id: ', conversation_id)

   # conversation = Conversation.objects.filter(users=request.user, id=conversation_id).first()

    data_input = DatasetandInput.objects.filter(conversation_id=conversation_id).first()

    data_input.datetime_column = date_column
    data_input.save()

    return JsonResponse({'Message': 'Successfully fetched date column'})



def identify_problem_type(request):

    problem_type = ''

    conversation_id = request.session.get('conversation_id')
    print('session conversation_id: ', conversation_id)

    data_input = DatasetandInput.objects.filter(conversation_id=conversation_id).first()


    data = pd.read_csv(data_input.file)

    if pd.api.types.is_numeric_dtype(data[data_input.target_variable]):

        print("data_input.datetime_column", type(data_input.datetime_column))
        # print(not data_input.datetime_column)
        # print(data_input.datetime_column.strip() == 'null')
        if not data_input.datetime_column or data_input.datetime_column.strip() == 'null':
            problem_type = 'numerical'
        else:
            problem_type = 'time series'
    else:
        problem_type = 'categorical'

    data_input.problem_type = problem_type
    data_input.inputcolumns = data.columns

    data_input.save()

    return JsonResponse({'problem_type': problem_type})



def send_inputs_to_api(request):
    api_url = "http://10.0.0.83:8000/run-pipeline/"
    conversation_id = request.session.get('conversation_id')
    data_input = DatasetandInput.objects.filter(conversation_id=conversation_id).first()

    if not data_input:
        return JsonResponse({'error': 'No data input found for the conversation ID.'}, status=400)

    try:
        with open(data_input.file.path, 'rb') as file:
            file_data = {'file': file}
            form_data = {
                'problem_type': data_input.problem_type,
                'target_variable': data_input.target_variable or 'None',
                'datetime_column': data_input.datetime_column or 'None'
            }

            print('form_data: ', form_data)
            print('file_data: ', file_data)

            response = requests.post(api_url, files=file_data, data=form_data)

        if response.status_code in {200, 202}:
            response_data = response.json()
            process_id = response_data.get('process_id')
            input_columns = response_data.get('inputcolumns')
            print('process_id: ', process_id)
            print('problem type: ', data_input.problem_type)
            Conversation.objects.filter(id=conversation_id).update(process_id=process_id)
            DatasetandInput.objects.filter(conversation_id=conversation_id).update(inputcolumns=input_columns)

            if not data_input.problem_type == "DocumentAnalysis" and not data_input.problem_type == "ImageAnalysis":
                print('request.user, conversation_id, process_id: ', request.user, conversation_id, process_id)
                get_process_logs(request.user, conversation_id, process_id)

            else:
                pkt_timezone = pytz.timezone('Asia/Karachi')
                pkt_time_now = timezone.now().astimezone(pkt_timezone)
                user_message = "User provided a Document!"
                resulting_text = "You provided Document file to analyze, I'm processing the Document!"
                conversation = Conversation.objects.filter(users=request.user, id=conversation_id).first()
                # Record message time in PKT
                message = Message.objects.create(
                    message=user_message,
                    sent_at=pkt_time_now,
                    conversation=conversation,
                    sender=request.user
                )

                bot_response = BotResponse.objects.create(
                    response_text=resulting_text,
                    created_at=pkt_time_now,
                    message=message
                )
            return JsonResponse({'message': 'File uploaded successfully.', 'process_id': process_id}, status=202)
        else:
            error_message = response.text if response.content else 'Unknown error'
            return JsonResponse({'error': f'Failed to upload file. Status code: {response.status_code}. {error_message}'}, status=response.status_code)

    except IOError as e:
        return JsonResponse({'error': f'Failed to read file for upload. {str(e)}'}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Failed to communicate with the pipeline API. {str(e)}'}, status=500)




# def get_process_logs(request):
#     api_url = "http://10.0.0.83:8000/get-processlogs/"
#
#     # process_id = request.GET.get('process_id')  # Correctly retrieve process_id from POST data
#     process_id=107
#     response = requests.get(api_url, {'process': process_id})
#     response_data = response.json()
#     print("response data: ", response_data)
#     message = response_data.get('message')
#     return JsonResponse({'message': message})


def get_process_logs(user, conversation_id, process_id):
    api_url = "http://10.0.0.83:8000/get-processlogs/"

    # Parse JSON data from the request body
    #data = json.loads(request.body)
    #conversation_id = request.session.get('conversation_id')
    #print('session conversation_id: ', conversation_id)
    #conversation = Conversation.objects.get(id=conversation_id)
    if not process_id:
        return JsonResponse({'error': 'No process ID provided'}, status=400)
    process_id = process_id
    # Send a GET request to the external API with process_id as a parameter
    try:
        response = requests.get(api_url, params={'process_id': process_id})
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        # Handle errors from requests or unsuccessful status codes
        return JsonResponse({'error': str(e)}, status=500)

    # Assuming the response returns JSON
    try:
        response_data = response.json()
        # Create a list of formatted strings containing the message and timestamp
        # Create a list of formatted strings containing the message and timestamp
        formatted_messages = [f"{entry['message']} {entry['timestamp']}" for entry in response_data]

        # Combine all formatted messages into a single string with each message on a new line
        resulting_text = '\n'.join(formatted_messages)

        # Now you can print or use the resulting_text as needed
        print(resulting_text)

        # Print each formatted message on a new line
        # Convert current UTC time to Pakistan Standard Time
        pkt_timezone = pytz.timezone('Asia/Karachi')
        pkt_time_now = timezone.now().astimezone(pkt_timezone)
        user_message = "User provided a Document!"
        conversation = Conversation.objects.filter(users=user, id=conversation_id).first()
        # Record message time in PKT
        message = Message.objects.create(
            message=user_message,
            sent_at=pkt_time_now,
            conversation=conversation,
            sender= user
        )


        bot_response = BotResponse.objects.create(
            response_text=resulting_text,
            created_at=pkt_time_now,
            message=message
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON response'}, status=500)

    # Extract message from response data, defaulting to 'No message' if not found
    #response = response_data

    return JsonResponse({'message': resulting_text})




def chat(request):
    pass