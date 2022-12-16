// setup
const loginChatContainer = document.querySelector('#login-chat-container');
const usernameInput = document.querySelector('#username');
const roomInput = document.querySelector('#room');
const ageInput = document.querySelector('#age');
const genderInput = document.querySelector('#gender');
const joinButton = document.querySelector('#join-button');

const chatTopic = document.querySelector('#chat-topic');
const chatContainer = document.querySelector('#chat-container');
const chatboard = document.querySelector('#chatboard');
const chatboardWrapper = document.querySelector('#chatboard-wrapper');
const userListContainer = document.querySelector('#user-list');
const chatMessageInput = document.querySelector('#chat-message-input');
const chatMessageButton = document.querySelector('#chat-send-button');
const baseurl = window.location.host + window.location.pathname;
//->

// app
let username;
let age;
let gender;
let room;
let socket;
let userList;
const websocketProtocol = window.location.protocol == 'https:' ? 'wss://' : 'ws://'
const endpoint = websocketProtocol + baseurl + 'ws/';

function defaultView()
{  
    chatContainer.style.display = 'none'; 
    loginChatContainer.style.display = 'block';
} defaultView();

function connectedView()
{
    chatContainer.style.display = 'block'; 
    loginChatContainer.style.display = 'none';
}

function cleanBoard()
{
    chatboard.innerHTML = '';
}

function updateRoomTopic()
{
    chatTopic.innerHTML = `#${roomInput.options[roomInput.selectedIndex].text} online: ${Object.keys(userList).length}`;
}

function addMessage(type, user, message)
{
    if (type == 'chat_message') 
    {
        const cssClass = (user == username) ? 'user-message my-message' : 'user-message';
        chatboard.innerHTML += `<p class="${cssClass}"><span>${user}</span>: ${message}</p>`;
    } else {
        chatboard.innerHTML += `<p class="log-message"> @ <span>${user}</span> ${message}</p>`;
    }

    chatboardWrapper.scrollTop = chatboardWrapper.scrollHeight;
}

function updateUserList(users)
{
    userList = JSON.parse(users);

    userListContainer.innerHTML = ''
    for (var user of userList) 
    {
        switch (user[1]) {
            case 1:
                icon = '&#xe87c';
                break;
            case 2:
                icon = '&#xf8da';
                break;
            default:
                icon = '&#xf8dd';
        }

        userListContainer.innerHTML += `<p id="user-${user[0]}" data-age="${user[2]}" class="gender-${user[1]}"><span class="material-symbols-outlined">${icon}</span> ${user[0]}</p>`;
    }
}

(function () {
    'use strict'
    loginChatContainer.addEventListener('submit', function (event) 
    {
        event.preventDefault();
        event.stopPropagation();
        username = usernameInput.value.trim();
        room=roomInput.value;
        gender=genderInput.value;
        age=ageInput.value;
        if(this.checkValidity()) {
            startConnetion();
            connectedView();
        }

        this.classList.add('was-validated');
    }, false)
  })()

function uuidGenerate()
{
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });

    return uuid;
}

function startConnetion()
{
    const queryString = '?username=' + username + '&gender=' + gender + '&age=' + age + '&uuid=' + uuidGenerate()
    socket = new WebSocket(endpoint + roomInput.value + queryString);

    socket.onopen = function(e) {
        cleanBoard();
    };
    
    socket.onclose = function(e) {
        defaultView();
    };
    
    socket.onerror = function(e) {
        defaultView();
    }
    
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        
        switch (data.type) {
            case "chat_message":
                addMessage(data.type, data.username, data.message);
                break;

            case "user_join":
                addMessage(data.type, data.username, 'join room')
                updateUserList(data.users_list);
                updateRoomTopic();
                break;

            case "user_leave":
                addMessage(data.type, data.username, 'left room');
                updateUserList(data.users_list);
                updateRoomTopic();
                break;
        }
    }
}

chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) chatMessageButton.click();
};

chatMessageButton.onclick = function(e) {
    e.preventDefault();

    const message = chatMessageInput.value;

    socket.send(JSON.stringify({
        'message': message,
        'username': username,
        'room': room
    }));

    chatMessageInput.value = '';
    return false;
}