$('header').css('padding','0')
$('.timestamp').hide()
timeStampHover()
function timeStampHover (){
  $('.timestamp').hide()
  $('.pull-left').each(function () {
      $(this).hover(function () {
          $(this).find('.timestamp').show();
          $(this).find('.message-text').hide();
          $(this).find('[data-livestamp]').css("background-color","red")
      },function(){
          $(this).find('.timestamp').hide();
          $(this).find('.message-text').show();
      } )
  });$('.pull-right').each(function () {
      $(this).hover(function () {
          $(this).find('.timestamp').show();
          $(this).find('.message-text').hide();
          $(this).find('[data-livestamp]').css("margin-left","-200px")
      },function(){
          $(this).find('.timestamp').hide();
            $(this).find('.message-text').show();
      } )
  });
}
function mozScroll (){
   setTimeout(function(){   $(document).scrollTop($(document).height());; }, 1);
}
      $('#newMessageAlert').hide()
      $('.messages').on("mousewheel", function() {
       console.log($(document).scrollTop());
   });
      var $details = $("#messages"),

          $messageHeight = $('.messages').height() - 324,
          $addMessageHeight = $(".add-message").height()
          $dynamicPosition = $messageHeight - $addMessageHeight

          $addMessage = $(".add-message"),
          $addMessagePos = $addMessage.position().top

          detailsPos = $details.position().top + $addMessagePos + 30; //need to create a variable
          $addMessage.css("position", "fixed").css("bottom",0);


      $(document).on("scroll", function() {
          if ($(document).scrollTop() >= $dynamicPosition){
              $addMessage.css("position", "static").css({"bottom":"10px"});

              }
          else{
              $addMessage.css("position", "fixed").css({"bottom":"0px","height":"40px", "margin-left": "10px"});
              }
      });

$("#messages").animate({ scrollTop: $("#messages").height() }, "slow");

        var base_ws_server_path = "{{ ws_server_path }}";
        $(document).ready(function () {
          roundMessRad()
            var websocket = null;
            var monitor = null;

            function initReadMessageHandler(containerMonitor, elem) {
              console.log('loaded')
                var id = $(elem).data('id');
                var elementWatcher = containerMonitor.create(elem);
                elementWatcher.enterViewport(function () {
                    var opponent_username = getOpponnentUsername();
                    var packet = JSON.stringify({
                        type: 'read_message',
                        session_key: '{{ request.session.session_key }}',
                        username: opponent_username,
                        message_id: id
                    });
                    $(elem).removeClass('msg-unread').addClass('msg-read');
                    websocket.send(packet);
                });
            }

            function initScrollMonitor() {

                var containerElement = $("#messages");
                var containerMonitor = scrollMonitor.createContainer(containerElement);
                $('.msg-unread').each(function (i, elem) {
                    if ($(elem).hasClass('opponent')){
                        initReadMessageHandler(containerMonitor, elem);

                    }

                });
                return containerMonitor
            }

            function getOpponnentUsername() {
                return "{{ opponent_username }}";
            }

            // TODO: Use for adding new dialog
            function addNewUser(packet) {
                $('#user-list').html('');
                packet.value.forEach(function (userInfo) {
                    if (userInfo.username == getUsername()) return;
                    var tmpl = Handlebars.compile($('#user-list-item-template').html());
                    $('#user-list').append(tmpl(userInfo))
                });
            }
            function roundMessRad(){
              $pullLeft = '.pull-left';
              $pullRight = '.pull-right';
              $(".row .msg-unread").each(function() {
  if (($(this).has($pullRight).length) && ($(this).next().has($pullLeft).length)){
    // find the parent and add class ONLY if the "IF" is true
    $(this).children($pullRight).css( {"border-bottom-right-radius": "20px"});
  }else if (($(this).has($pullRight).length) && ($(this).prev().has($pullLeft).length)){
    $(this).children($pullRight).css( {"border-top-right-radius": "20px","border-bottom-right-radius": "0px"} );
  }else if (($(this).has($pullRight).length) && ($(this).prev().has($pullRight).length) && ($(this).next().has($pullRight).length)){
    $(this).children($pullRight).css( {"border-top-right-radius": "0px","border-bottom-right-radius": "0px"} );
  }
});

            }
            function addNewMessage(packet) {

              $("#senderPacket").val(packet['sender_name'])
                var msg_class = "";
                if (packet['sender_name'] != $("#owner_username").val()) {
                    msg_class = "pull-left";

                } else {
                    msg_class = "pull-right";
                }
                var msgElem =
                    $('<div class="row msg-unread" data-id="' + packet.message_id + '">' +
                        '<p class="' + msg_class + '">' +
                        '<span class="username">' + packet['sender_name'] + ': </span>' +
                        packet['message'] +
                        ' <span class="timestamp">&ndash; <span data-livestamp="' + packet['created'] + '"> ' + packet['created'] + '</span></span> ' +
                        '</p> ' +
                        '</div>');
                $('#messages').append(msgElem);

                scrollToLastMessage()
                newMessageAlert()
                roundMessRad()
                timeStampHover()
                mozScroll()
            }
            function newMessageAlert(){
$('#newMessageAlert').show()
var audio = new Audio('{% static "sounds/new-message.mp3" %}')
  audio.play()
            }
            function scrollToLastMessage() {
              console.log("scrollToLastMessage Loaded")
                var $msgs = $('#messages');
                $msgs.animate({"scrollBottom": $msgs.prop('scrollHeight')})

            }

            function generateMessage(context) {
                var tmpl = Handlebars.compile($('#chat-message-template').html());
                return tmpl({msg: context})
            }

            function setUserOnlineOffline(username, online) {
                var elem = $("#user-" + username);
                if (online) {
                    elem.attr("class", "btn btn-success");
                } else {
                    elem.attr("class", "btn btn-danger");
                }
            }

            function gone_online() {
                $("#offline-status").hide();
                $("#online-status").show();
            }

            function gone_offline() {
                $("#online-status").hide();
                $("#offline-status").show();

            }

            function flash_user_button() {
                var btn = $("#flash");
                btn.fadeTo(700, 0.1, function () {
                    $(this).fadeTo(800, 1.0);
                });
            }

            function setupChatWebSocket() {

                var opponent_username = getOpponnentUsername();
                websocket = new WebSocket(base_ws_server_path + '{{ request.session.session_key }}/' + opponent_username);
				console.log(websocket)
                websocket.onopen = function (event) {
                    var opponent_username = getOpponnentUsername();

                    var onOnlineCheckPacket = JSON.stringify({
                        type: "check-online",
                        session_key: '{{ request.session.session_key }}',
                        username: opponent_username
                        //{                      Sending username because the user needs to know if his opponent is online }
                    });
                    var onConnectPacket = JSON.stringify({
                        type: "online",
                        session_key: '{{ request.session.session_key }}'

                    });

                    console.log('connected, sending:', onConnectPacket);
                    websocket.send(onConnectPacket);
                    console.log('checking online opponents with:', onOnlineCheckPacket);
                    websocket.send(onOnlineCheckPacket);
                    monitor = initScrollMonitor();
                    console.log("Monitor", monitor)
                };


                window.onbeforeunload = function () {

                    var onClosePacket = JSON.stringify({
                        type: "offline",
                        session_key: '{{ request.session.session_key }}',
                        username: opponent_username,
                        //{# Sending username because to let opponnent know that the user went offline #}
                    });
                    console.log('unloading, sending:', onClosePacket);
                    websocket.send(onClosePacket);
                    websocket.close();

                };


                websocket.onmessage = function (event) {
                    var packet;

                    try {
                        packet = JSON.parse(event.data);
                        console.log(packet)
                    } catch (e) {
                        console.log(e);
                    }

                    switch (packet.type) {
                        case "new-dialog":
                            // TODO: add new dialog to dialog_list
                            break;
                        case "user-not-found":
                            // TODO: dispay some kind of an error that the user is not found
                            break;
                        case "gone-online":
                            if (packet.usernames.indexOf(opponent_username) != -1) {
                                gone_online();
                            } else {
                                gone_offline();
                            }
                            for (var i = 0; i < packet.usernames.length; ++i) {
                                setUserOnlineOffline(packet.usernames[i], true);
                            }
                            break;
                        case "gone-offline":
                            if (packet.username == opponent_username) {
                                gone_offline();
                            }
                            setUserOnlineOffline(packet.username, false);
                            break;
                        case "new-message":
                        var senderName = packet['sender_name']
                         if($('body').hasClass('modal-open')) {


                           return true
                         }
                         else{
                          $("#"+senderName+"").click()
                        $("#senderPacket").val(senderName)}


                            if (packet['sender_name'] == opponent_username || packet['sender_name'] == $("#owner_username").val()) {
                                addNewMessage(packet);

                                if (packet['sender_name'] == opponent_username) {
                                    initReadMessageHandler(monitor, $("div[data-id='" + packet['message_id'] + "']"));

                                }

                            } else {
                                flash_user_button();


                            }
                            break;
                        case "opponent-typing":
                            var typing_elem = $('#typing-text');
                            if (!typing_elem.is(":visible")) {
                                typing_elem.fadeIn(500);
                            } else {
                                typing_elem.stop(true);
                                typing_elem.fadeIn(0);
                            }
                            typing_elem.fadeOut(3000);
                            break;
                        case "opponent-read-message":
                            if (packet['username'] == opponent_username) {
                                $("div[data-id='" + packet['message_id'] + "']").removeClass('msg-unread').addClass('msg-read');
                            }
                            break;

                        default:
							setUserOnlineOffline(packet.username, true);
                            console.log('error: ', event)
                    }
                }
            }

            function sendMessage(message) {
                var opponent_username = getOpponnentUsername();
                var newMessagePacket = JSON.stringify({
                    type: 'new-message',
                    session_key: '{{ request.session.session_key }}',
                    username: opponent_username,
                    message: message
                });


                websocket.send(newMessagePacket)
            }

            $('#chat-message').keypress(function (e) {
                if (e.which == 13 && this.value) {
                    sendMessage(this.value);
                    this.value = "";
                    return false
                } else {
                    var opponent_username = getOpponnentUsername();
                    var packet = JSON.stringify({
                        type: 'is-typing',
                        session_key: '{{ request.session.session_key }}',
                        username: opponent_username,
                        typing: true
                    });
                    websocket.send(packet);
                }

            });


            $('#btn-send-message').click(function (e) {
                var $chatInput = $('#chat-message');
                var msg = $chatInput.val();
                if (!msg) return;
                sendMessage($chatInput.val());
                $chatInput.val('')
            });

          setupChatWebSocket();


            scrollToLastMessage();
        });
