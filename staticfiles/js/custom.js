let conversationId; // Declare conversationId as a global variable

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



const csrftoken = getCookie('csrftoken');

let form = document.querySelector(".submit-form");
let input = document.querySelector("#input_value");
let heading = document.querySelector("#main-header");
let container = document.querySelector(".container-fluid-2");
let spinner = document.querySelector(".spinner-main");

form.addEventListener("submit", submitForm);

// Inside the submitForm function
function submitForm(e) {
    e.preventDefault();
    let message = input.value;

    let msg = document.querySelector('.success-msg');
    if (msg){
        msg.innerHTML = '';
    }

    container.innerHTML += `
        <div class="chat-container"></div>
    `;

    const chatContainer = document.querySelector('.chat-container');
    chatContainer.innerHTML += `
        <div class="user-chat-container">
            <div class="user-pic"><i class="fa-solid fa-circle-user"></i></div>
            <div class="user-message">${message}</div>
        </div>
    `;
    input.value = "";
    const data = { msg: message, conv: conversationId }; // Include conversation ID in the data

    postJSON(data);
}

async function postJSON(data) {
    spinner.style.display = "flex";
    const url = "/get-value";

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        console.log("result: ", result);

        // Update the conversation ID in the JavaScript variable
        if (result.conv) {
            conversationId = result.conv;
        }

        if (result.columns){
            console.log('result.columns: ', result.columns)
            showInputvaluesModal(result.columns, data.msg);
        } else {
            // Append the bot's response to the chat container
            const chatContainer = document.querySelector('.chat-container');

            chatContainer.innerHTML += `
                <div class="bot-chat-container">
                    <div class="bot-icon"><i class="fa-solid fa-robot"></i></div>
                    <div class="bot-response">${result.res}</div>
                </div>
            `;

            // Hide loading indicators and reset input field
            heading.style.display = "none";
            spinner.style.display = "none";
            input.value = "";

            console.log("Success:", result);
        }

    } catch (error) {
        console.error("Error:", error);
        // Optionally, handle the error in UI
        chatContainer.innerHTML += `
            <div class="bot-chat-container">
                <div class="bot-icon"><i class="fa-solid fa-robot"></i></div>
                <div class="bot-response">Error retrieving response.</div>
            </div>
        `;
        spinner.style.display = "none";
    }
}

function showInputvaluesModal(columns, userMessage) {
    console.log('showInputvaluesModal');
    const modal = document.querySelector('#selectionVariableModal');
    let formContent = `<input type="hidden" id="originalUserMessage" value="${userMessage}">`;

    columns.forEach(column => {

        formContent += `
            <div class="form-group">
                <label for="${column}">${column}</label>
                <input type="text" class="form-control" id="${column}" name="${column}">
            </div>
        `;
    });

    modal.innerHTML = `
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="problemTargetModalLabel">Select Variables</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="inputColumnsForm">
                        ${formContent}
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" onclick="handleColumnValues()">Save changes</button>
                </div>
            </div>
        </div>
    `;

    // Show the modal (assuming you are using Bootstrap)
    $(modal).modal('show');
}

function handleColumnValues() {
    const form = document.getElementById('inputColumnsForm');
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    console.log('input data', data); // Handle the collected data as needed

    fetch('/get_input_json/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Make sure to include the CSRF token if necessary
        },
        body: JSON.stringify({columns: data})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data['message']);
        // Handle the response from the server
        // Trigger the initial request again with the original message
        let originalUserMessage = document.getElementById('originalUserMessage').value;
        postJSON({ msg: originalUserMessage, conv: conversationId });
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Close the modal (assuming you are using Bootstrap)
    $('#selectionVariableModal').modal('hide');
}


//async function new_chat(){
//    const url = "/new_chat";
//    try {
//        const response = await fetch(url, {
//            method: "get",
//            headers: {
//                "Content-Type": "application/json",
//                'X-CSRFToken': csrftoken
//            },
//            body: JSON.stringify(data),
//        });
//
//        const result = await response.json();
//        console.log("result: ", result);
//    } catch (error) {
//        console.error("Error:", error);
//    }
//
//}



function onNewChat() {
    fetch('/new_chat', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to create new chat');
        }
        return response.json(); // Parse JSON response

    })
    .then(data => {
        // Update conversationId with the new conversation ID
        conversationId = data.conversation_id;

        console.log('data.conversation_id: ', conversationId);

        // Clear the chat container
        let user_chat_container = document.querySelector(".user-chat-container");

        let bot_chat_container = document.querySelector(".bot-chat-container");

        let chatContainer = document.querySelector('.chat-container');

        // Check if the chat container exists
        if (user_chat_container && bot_chat_container && chatContainer) {
            // Clear existing content
            chatContainer.innerHTML = '';
            user_chat_container.innerHTML = '';
            bot_chat_container.innerHTML = '';
//            container.innerHTML = '';
        }

        let file_upload_div = document.querySelector('.file_upload_div');
        if (file_upload_div){
            file_upload_div.innerHTML = `<div style="width: 500px;height: 40px;display: flex;align-items: center;
                   justify-content: center; align-items: center;padding: 0px 10px 0px 10px, margin-top:40px;
                  ">
                  <input type="file" id="fileInput" accept=".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                  <button id="attachment-btn"><i class="fa-solid fa-upload"></i></button>
            </div>`;
            document.getElementById('attachment-btn').addEventListener('click', onUploadFile);
        }



    })
    .catch(error => {
        console.error('Error creating new chat:', error);
    });
}


function test(){

    console.log('test api')
    const url = 'http://10.0.0.83:8000/run-pipeline/';

    // JSON data to be passed
    const jsonData = {
        key1: 'value1'
        // Add more data as needed
    };

    // Make a POST request with JSON data
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse response JSON
    })
    .then(data => {
        // Handle response data
        console.log('Response:', data);
    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);
    });
}


document.addEventListener("DOMContentLoaded", function() {

//    test()

    fetch('/getConversationID')
    .then(response => response.json())
    .then(data=>{
        conversation_id = data.conversation_id
        console.log('Conv id:', conversation_id);
        add_message_and_responses(conversation_id)

    })
    .catch(error => console.error('Error fetching conversation data:', error));

    const conversationLinks = document.querySelectorAll('.conversation-link');
    conversationLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const conversation_id = this.getAttribute('data-conversation-id');

            update_conversation_id(conversation_id)

            add_message_and_responses(conversation_id)
        });
    });
});


function add_message_and_responses(conversation_id){
    fetch(`/conversation/${conversation_id}/`)
    .then(response => response.json())
    .then(data => {
        console.log('conversationId: ', conversation_id)
        console.log('Data:', data); // Log data for debugging

        conversationId = conversation_id;


//        let container = document.querySelector(".container-fluid-2");

        // Check if the chat container exists
        if (container) {
//
//            container.innerHTML = '';
//
//            container.innerHTML = `<div class="chat-container"></div>`

            let chatContainer = document.querySelector(".chat-container");
            chatContainer.innerHTML='';

            // Iterate over messages and bot responses simultaneously
            for (let i = 0; i < data.messages.length || i < data.bot_responses.length; i++) {
                // Append user message
                if (i < data.messages.length) {
                    chatContainer.innerHTML += `
                        <div class="user-chat-container">
                            <div class="user-pic"><i class="fa-solid fa-circle-user"></i></div>
                            <div class="user-message">${data.messages[i].text}</div>
                        </div>
                    `;
                }
                // Append bot response
                if (i < data.bot_responses.length) {
                    chatContainer.innerHTML += `
                        <div class="bot-chat-container">
                            <div class="bot-icon"><i class="fa-solid fa-robot"></i></div>
                            <div class="bot-response">${data.bot_responses[i][0].response_text}</div>
                        </div>
                    `;
                }
            }
        } else {
            console.error('Chat container not found.');
        }
    })
    .catch(error => console.error('Error fetching conversation data:', error));

}


async function update_conversation_id(conversationId){
    const url = "/update-conversation-id";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({conversation_id:conversationId}),
        });

        const result = await response.json();
        console.log("result: ", result);

    } catch (error) {
        console.error("Error:", error);
    }
}


var fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = '.csv,.xlsx';
fileInput.style.display = 'none'; // Hide the file input element
document.body.appendChild(fileInput);

// Handle button click event



function onUploadFile(e) {
    // Trigger click event on the file input element
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Get CSRF token from the cookie
        const csrftoken = getCookie('csrftoken');

        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken // Include CSRF token in the headers
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('File uploaded successfully');
                // If you expect the server to respond with JSON data including a 'problem_type' property:
                return response.json();
            } else {
                console.log('File upload failed');
                // Handle error
                throw new Error('File upload failed');
            }
        })
        .then(data => {

            file_upload_div = document.querySelector('.file_upload_div');
            file_upload_div.innerHTML='';
            // If the server responds with JSON data
            console.log("problem_type:", data['problem_type']);
            if (data['problem_type'] == "DocumentAnalysis" || data['problem_type'] == "ImageAnalysis"){
                pipeline_inputs()
            }
            else if (data['problem_type'] == null)
            {
                modal = document.querySelector('#selectionVariableModal');

                fetch('/get_column_names/')
                    .then(response => response.json())
                    .then(data => {
                        console.log('Data:', data.column_names);

                        var column_names = data.column_names;

                        // Check if column_names is an array
                        console.log('Column names:', column_names);

                        spinner.style.display = "flex";

                        modal.innerHTML = `<div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="problemTargetModalLabel">Select Variables</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <form>
                                        <div class="form-group">
                                            <label for="targetVariable">Target Variable</label>
                                            <select class="form-control" id="targetVariable">
                                                ${column_names.map(column_name => `<option value="${column_name}">${column_name}</option>`).join('')}
                                            </select>
                                        </div>
                                    </form>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary" onclick="handleTargetSelection()">Save changes</button>
                                </div>
                            </div>
                        </div>`;

                        $('#selectionVariableModal').modal('show');

                    })
                    .catch(error => {
                        console.error('Error getting column names:', error);
                    });
                }

            else {
                console.error('Failed to upload file');
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
    } else {
        console.error('No file selected');
    }
}


async function handleTargetSelection() {

   console.log('selection handled!')
   var selectElement = document.getElementById("targetVariable");

    // Get the selected option
    var selectedOption = selectElement.options[selectElement.selectedIndex].value;

    // Do something with the selected option, for example, log it to the console
    console.log("Selected option:", selectedOption);

    $('#selectionVariableModal').modal('hide');


    // Get the CSRF token from the cookie
    var csrftoken = getCookie('csrftoken');

    const url = "/get_selected_target_var";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({target_var: selectedOption}),
        });

        const result = await response.json();
        console.log("result: ", result);

        if (result['isNumeric']){

            console.log('is numeric')

            date_columns = result['date_columns']
            if (date_columns != []){
                modal = document.querySelector('#selectionVariableModal');
                modal.innerHTML = `
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="problemTargetModalLabel">Select Variables</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <form>
                                <div class="form-group">
                                    <label for="targetVariable">Date Variable</label>
                                    <select class="form-control" id="targetVariable">
                                        ${date_columns.map(column_name => `<option value="${column_name}">${column_name}</option>`).join('')}
                                    </select>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" onclick="handleTimeVarSelection()">Save changes</button>
                        </div>
                    </div>
                </div>`;
            }
        }else{
           console.log('not numeric')
           analyze_problem_type()
        }

        $('#selectionVariableModal').modal('show');


    }
    catch(error) {
        console.error('Error posting target variable:', error);
    }
}


function analyze_problem_type(){

    fetch('/identify_problem_type/')
    .then(response => response.json())
    .then(data => {
        console.log('Problem Type:', data['problem_type']);

        pipeline_inputs()
    })
    .catch(error => {
        console.log("Error identifying problem type: ", error);
    })

}


function pipeline_inputs(){
    var url = 'send_inputs_to_api';

    // Perform a Fetch request to trigger the Django view function
    fetch(url, {
        method: "GET", // Use "POST" method since we are sending data to the server
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to fetch process ID");
        }
        // Parse the JSON response
        return response.json();
    })
    .then(data => {
        // Access the process_id from the response
        const process_id = data['process_id'];
        console.log("Process ID:", process_id);

//        fetch_process_logs(process_id)
        // Use the process_id as needed in your JavaScript code

        spinner.style.display="none";
        container.innerHTML+=`
        <div class = 'success-msg' style='display:flex;justify-content:center;'><h5>File processed successfully</h5></div>
        `
    })
    .catch(error => {
        console.error("Failed to trigger API:", error);
    });
}



function fetch_process_logs(process_id){
    var url = 'get_process_logs'
    fetch(url, {
        method:'POST',
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({process_id: process_id}),
    })
    .then(response => {
        if(!response.ok){
            console.log('Failed to fetch process logs');
            throw new Error('Failed to fetch process logs');
        }
        return response.json(); // Parse JSON data from the response
    })
    .then(data => {
        message = data['message'];
        console.log("Message:", message);
        container.innerHTML = `
            <h4>${message}</h4>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error, show error message to the user, etc.
    });
}




async function handleTimeVarSelection(){
    console.log('handle date col selection')

    var selectElement = document.getElementById("targetVariable");

    // Get the selected option
    var selectedOption = selectElement.options[selectElement.selectedIndex].value;

    // Do something with the selected option, for example, log it to the console
    console.log("Selected option:", selectedOption);

    $('#selectionVariableModal').modal('hide');

    // Get the CSRF token from the cookie
    var csrftoken = getCookie('csrftoken');

    const url = "/get_date_column";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({date_column: selectedOption}),
        });
        if (response.ok) {
            const responseData = await response.json();
            console.log('response: ', responseData['Message']);

            analyze_problem_type()

        } else {
            // If response is not successful, throw an error
            throw new Error('Network response was not ok.');
        }
    }
    catch(error) {
        console.error('Error posting target variable:', error);
    }

}


// Handle file selection change
//fileInput.addEventListener('change', function() {
//    // Get the selected file
//    var file = this.files[0];
//
//    // Create a folder name (you can customize this)
//    var folderName = "SelectedFiles";
//
//    // Create a new folder
//    createFolder(folderName, function(folder) {
//        // Save the file into the folder
//        saveFileIntoFolder(folder, file);
//    });
//});
//
//// Function to create a folder
//function createFolder(folderName, callback) {
//    // You would need to implement this function based on your environment
//    // In a browser environment, you cannot directly create folders due to security restrictions
//    // However, you can simulate folder creation by handling file organization on the client side
//
//    // For demonstration, let's assume folder creation is simulated by alerting the folder name
//    alert("Folder created: " + folderName);
//
//    // Call the callback function with the folder object
//    callback(folderName);
//}
//
//// Function to save the file into a folder
//function saveFileIntoFolder(folder, file) {
//    // You would handle the actual file saving based on your environment
//    // In a browser environment, you would typically use File API to read the file content
//    // and then perform actions like sending it to a server or storing it locally
//
//    // For demonstration, let's just log the folder name and file name
//    console.log("File saved into folder:", folder);
//    console.log("File name:", file.name);
//}

