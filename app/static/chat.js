// Chat system

// Contains the loops and their state
var LoopStates = {};

// Defines whether the chat should be scrolled to the bottom or not
var scrollBool = true;

// Defines all states a loop can have
const State = {
    OFF: 0,
	MONITOR: 1,
	WRITE: 2
}

// Defines the color of a loop for each state
const StateColor = {
    0: "#ffffff",
    1: "#778899",
    2: "#2F4F4F"
}

/*
Getter for LoopStates
*/
function getLoopStates () {
  return LoopStates
}

/*
Toggles the visibility of the chat window if the chat icon is clicked
*/
function toggleDisplay () {
    const chatWindow = document.getElementById("chat-div")

    if (chatWindow.classList.contains("d-none")) {
        $("#chat-div").removeClass("d-none").addClass("d-block")
        $("#load-messages-div").removeClass("d-none").addClass("d-block")

        var chatIconBadge = $('#chat-icon-badge')
        var chatBody = $('#chat-body')

        if (chatIconBadge.hasClass('visible')) {
            chatIconBadge.removeClass('visible').addClass('invisible')
            chatBody.scrollTop(chatBody.get(0).scrollHeight);
        }
    } else {
        $("#chat-div").removeClass("d-block").addClass("d-none")
        $("#load-messages-div").removeClass("d-block").addClass("d-none")
    }
}

/*
Changes the state of a loop if the loop is clicked. Depending on the current state of the loop
the new state is set
*/
function changeLoopState(element) {
    var parent = element.parentNode
    var grandparent = parent.parentNode
    var loopId = grandparent.id.toString()
    var loopCard = $('#' + loopId)

    switch (LoopStates[loopId]) {
        case State.MONITOR:

            if (loopCard.attr('data-full-access') === "True") {
                if (Object.values(LoopStates).includes(State.WRITE)) {
                    var activeLoop = Object.keys(LoopStates).find(key => LoopStates[key] === State.WRITE).toString();
                    console.log("This loop is already active: " + activeLoop)

                    changeToMonitor(activeLoop)
                    changeToWrite(loopId)

                } else if (!(Object.values(LoopStates).includes(State.WRITE))) {
                    changeToWrite(loopId)
                }
            }

            break

        case State.WRITE:
            changeToMonitor(loopId)
            setActiveLoop('')
            $('#chatFormControlTextArea').prop("disabled", true)
            var send_icon = $('#send-icon')
            if (!(send_icon.hasClass('nohover'))) {
                send_icon.addClass('nohover')
            }
            break

        default:
            changeToMonitor(loopId)
            $('#' + element.id.toString()).trigger("join", loopId)
    }
}

/*
Changes the state of a loop to OFF after the dedicated OFF-Button is clicked
*/
function setLoopOff (element) {
    var parent = element.parentNode
    var grandparent = parent.parentNode
    var greatgrandparent = grandparent.parentNode
    var loopId = greatgrandparent.id.toString()

    var loopCard = $('#' + loopId)

    $('#' + element.id.toString()).trigger("leave", loopId)

    if (getActiveLoop() === loopId) {
        setActiveLoop('')
        $('#chatFormControlTextArea').prop("disabled", true)
        var send_icon = $('#send-icon')
        if (!(send_icon.hasClass('nohover'))) {
            send_icon.addClass('nohover')
        }
    }

    var chatBody = $("#chat-body");
    var oldmessageElements = chatBody.children('.message-container').detach().get()
    var messageElements = []

    oldmessageElements.forEach(function (a) {
        if ($(a).attr("data-message-loop") !== loopId) {
            messageElements.push(a)
        }
    })
    chatBody.append(messageElements)

    LoopStates[loopId] = State.OFF
    loopCard.css("background", StateColor[State.OFF.toString()])
    loopCard.css("color", "#000000")
    
    if (!((Object.values(LoopStates).includes(State.WRITE)) || (Object.values(LoopStates).includes(State.MONITOR)))) {
        $("#load-messages").css("pointer-events", "none")
    }
}

/*
Changes the state of a loop to MONITOR and updates the background color accordingly
*/
function changeToMonitor(loopId) {
    var loopCard = $('#' + loopId)

    LoopStates[loopId] = State.MONITOR
    loopCard.css("background", StateColor[State.MONITOR.toString()])
    loopCard.css("color", "#ffffff")

    var loadMessagesElement = $("#load-messages")

    if (loadMessagesElement.attr("style")) {
        loadMessagesElement.removeAttr("style")
    }
}

/*
Changes the state of a loop to WRITE and updates the background color accordingly
*/
function changeToWrite(loopId) {
    var loopCard = $('#' + loopId)

    setActiveLoop(loopId)
    $('#chatFormControlTextArea').prop("disabled", false)
    var send_icon = $('#send-icon')
    if (send_icon.hasClass('nohover')) {
        send_icon.removeClass('nohover')
    }

    LoopStates[loopId] = State.WRITE
    loopCard.css("background", StateColor[State.WRITE.toString()])
    loopCard.css("color", "#ffffff")
}

/*
Scrolls the chat to the bottom if the booleans are true and notifies the user if scrolling 
is not executed because the user is reading older messages
*/
function updateScrolling(oldMessages) {
    if (scrollBool) {
        var chatBody = $('#chat-body')

        chatBody.scrollTop(chatBody.get(0).scrollHeight);
    } else {
        if (!(oldMessages)) {
            $('#chat-icon-badge').removeClass("invisible").addClass("visible")
            $("#scroll-down-div").removeClass("d-none").addClass("d-block")
        }
    }
}

/*
Sets the boolean to whether it should be scrolled or not
*/
function shouldScroll() {
    var chatBody = $('#chat-body')

    scrollBool = (chatBody.get(0).scrollHeight - chatBody.get(0).offsetHeight <= chatBody.scrollTop())
}

/*
Allows to scroll to the bottom of the chat window manually by clicking scroll-down arrows 
after they appear
*/
function scrollBottom() {
    var chatBody = $('#chat-body')
    chatBody.animate({ scrollTop: chatBody.get(0).scrollHeight },  5);

    if (!(chatBody.get(0).scrollHeight - chatBody.get(0).offsetHeight <= chatBody.scrollTop())) {
        $('#chat-icon-badge').removeClass("visible").addClass("invisible")
        $("#scroll-down-div").removeClass("d-block").addClass("d-none")
    }
}

/*
Changes the icon while loading old messages from the reload button to a spinning wheel and back
*/
function toggleLoadPreviousMessages() {
    var loadMessagesElement = $("#load-messages")

    if (loadMessagesElement.attr('data-loading') === "False") {
        loadMessagesElement.html('<span class="spinner-border" role="status" aria-hidden="true"></span>')
        loadMessagesElement.css("pointer-events", "none")
        loadMessagesElement.attr('data-loading', "True")
    } else if (loadMessagesElement.attr('data-loading') === "True") {
        loadMessagesElement.html('<i class="fa-solid fa-arrows-rotate fa-2xl" id="load-messages-icon"></i>')
        loadMessagesElement.removeAttr("style")
        loadMessagesElement.attr('data-loading', "False")
    }
}
