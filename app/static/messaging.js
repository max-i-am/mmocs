// Messaging
/*
Messaging with SocketIO using WebSockets only and TLS for security.
*/

// Contains the SocketIO connection
var socket

// Contains the current position of the user
var position = $('#page-header-chat').attr('data-position')

// Contains the current active loop (Writing state)
var activeLoop = ''

// Contains the id "loop-state-link" to monitor if a loop changed
var loopLink = $('#loop-state-link')

/*
Setter for activeLoop variable
*/
function setActiveLoop (loopId) {
  activeLoop = loopId
}

/*
Getter for activeLoop variable
*/
function getActiveLoop () {
  return activeLoop
}

/*
Escapes unsafe message text to prevent HTML misinterpretation
*/
const escapeHtml = (unsafe) => {
    return unsafe.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
}

/*
Checks if the current position of the user is mentioned in the message
*/
const checkMention = (escapedMessage) => {
  var firstWord = escapedMessage.split(' ', 1)

  if (Array.from(firstWord[0])[0] === "@" && firstWord[0].split('').slice(1).join('') === position) {

    escapedMessage = escapedMessage.split(' ').slice(1).join(' ')
    var boldFirstWord = "<strong>" + firstWord + "</strong>"
    return  boldFirstWord + ' ' + escapedMessage
  }

  return escapedMessage
}

/*
All client side functions of SocketIO. Executed after the JavaScript environment is ready
*/
$(document).ready(function () {
  console.log("ready!")

  /*
  Tries to connect the client with the server through SocketIO using Websocket
  */
  socket = io.connect('https://' + document.domain + ':' + location.port, {transports: ['websocket']});

  /*
  Connect event which is received after successful connection establishment
  */
  socket.on('connect', function () {
    console.log("Connected!")
  })

  /*
  Emits join event to join the selected loop
  */
  loopLink.on('join', function (e, loop) {
    socket.emit('join', {loop: loop})
  })

  /*
  Emits the load-messages event with selected loops (Reading state, Writing state)
  */
  $('#load-messages').on('click', function (e) {
    var loopStates = getLoopStates()
    var monitoringLoops = Object.keys(loopStates).filter(key => loopStates[key] > State.OFF)

    socket.emit('load-messages', {loops: monitoringLoops})
  })

  /*
  Sends the message after the send button is clicked with metadata such as loop and temporary messsage ID.
  Additionally, the sent message is displayed with the current time in the chat window
  */
  $('#send-icon').on('click', function (e) {
    var chatInputField = $('#chatFormControlTextArea')
    var message = chatInputField.val()

    if (message) {
      var time = new Date()
      var timeString = time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})

      // Creates temporary random number until the server sends final UUID, which replaces the temporary message ID
      var tmpMessageId = Date.now() + Math.random()

      shouldScroll()

      $('#chat-body').append(
          '<div class="message-container d-flex flex-column justify-content-end" data-date=' + time.toISOString() + ' data-messageid=' + tmpMessageId + ' data-message-loop=' + activeLoop + '><p class="small p-2 ms-auto mb-1 text-white rounded-3" style="background-color: cornflowerblue; display: inline-block; word-break: break-all; overflow-wrap: break-word; word-wrap: break-word; hyphens: auto;">' + escapeHtml(message) + '</p><p class="small ms-auto mb-3 rounded-3 text-muted d-flex justify-content-end">' + activeLoop + ' | ' + timeString + '</p></div>'
      )

      updateScrolling(false)
      
      socket.emit('message', {loop: activeLoop, tmpMessageId: tmpMessageId, message: message})

    }

    // Resets the input field after the message is sent
    chatInputField.val('')
  })

  /*
  Acknowledgement event which contains the message ID created by the server to replace the temporary message ID
  */
  socket.on('ack-with-messageid', function (ack) {
    var chatElement = $("#chat-body").find('[data-messageid="' + ack[0] + '"]')
    chatElement.attr('data-messageid', ack[1])

  })

  /*
  Event for an incoming message, which displays the message in the chat window and scrolls to the bottom if necessary
  */
  socket.on('message', function (message) {
    var time = new Date()
    var timeString = time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})

    var chatDiv = $('#chat-div')
    var chatBody = $('#chat-body')

    if (chatDiv.hasClass('d-none')) {
      $('#chat-icon-badge').removeClass("invisible").addClass("visible")
    }
    
    shouldScroll()

    chatBody.append(
        '<div class="message-container d-flex flex-column justify-content-start" id="testing-0" data-date=' + time.toISOString() + ' data-messageid=' + message.messageid + ' data-message-loop=' + message.loop + '><p class="small p-2 me-auto mb-1 rounded-3" style="background-color: #f5f6f7; display: inline-block; word-break: break-all; overflow-wrap: break-word; word-wrap: break-word; hyphens: auto;">' + checkMention(escapeHtml(message.message)) + '</p><p class="small me-auto mb-3 rounded-3 text-muted">' + message.position + ' | ' + message.loop + ' | ' + timeString + '</p></div>'
    )

    updateScrolling(false)
  })

  /*
  Event for receiving old messages, which displays the messages at the correct time in the chat window.
  Additionally, the chat window is scrolled to the bottom if necessary
  */
  socket.on('old-messages', async function (message) {
    var chatBody = $("#chat-body");

    var differentMessageIDs = chatBody.children('.message-container').map(function () {
      return $(this).attr("data-messageid")
    }).toArray()

    var messageDivs = []

    // Check if messages are in the response
    if (!(Object.keys(message).length === 0)) {

      for (const messageKey in message) {

        // Check if message is a duplicate message of an already loaded message
        if (!(differentMessageIDs.includes(messageKey))) {

          var time = new Date(message[messageKey][3] + "+00:00")
          var timeString = time.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
          
          if (position === message[messageKey][1]) {
            messageDivs.push('<div class="message-container d-flex flex-column justify-content-end" data-date=' + time.toISOString() + ' data-messageid=' + messageKey + ' data-message-loop=' + message[messageKey][2] + '><p class="small p-2 ms-auto mb-1 text-white rounded-3" style="background-color: cornflowerblue; display: inline-block; word-break: break-all; overflow-wrap: break-word; word-wrap: break-word; hyphens: auto;">' + escapeHtml(message[messageKey][0]) + '</p><p class="small ms-auto mb-3 rounded-3 text-muted d-flex justify-content-end">' + message[messageKey][2] + ' | ' + timeString + '</p></div>')
          } else {
            messageDivs.push('<div class="message-container d-flex flex-column justify-content-start" data-date=' + time.toISOString() + ' data-messageid=' + messageKey + ' data-message-loop=' + message[messageKey][2] + '><p class="small p-2 me-auto mb-1 rounded-3" style="background-color: #f5f6f7; display: inline-block; word-break: break-all; overflow-wrap: break-word; word-wrap: break-word; hyphens: auto;">' + checkMention(escapeHtml(message[messageKey][0])) + '</p><p class="small me-auto mb-3 rounded-3 text-muted">' + message[messageKey][1] + ' | ' + message[messageKey][2] + ' | ' + timeString + '</p></div>')
          }
          
        }
      }

      shouldScroll()

      var messageElements = chatBody.children('.message-container').detach().get()

      var allMessageElements = messageDivs.concat(messageElements)

      allMessageElements.sort(function(a, b) {
        return new Date($(a).attr("data-date")) - new Date($(b).attr("data-date"));
      })

      chatBody.append(allMessageElements)
    }

    updateScrolling(true)

    toggleLoadPreviousMessages()
  })

  /*
  Emits leave event to leave the selected loop
  */
  loopLink.on('leave', function (e, loop) {
    socket.emit('leave', {loop: loop})
  })

  /*
  Disconnect event for stopping the SocketIO connection
  */
  socket.on('disconnect', function () {
    console.log("Disconnected!")
  })
})