// https://stackoverflow.com/a/42591519
if (location.hash) {
  $('a[href=\'' + location.hash + '\']').tab('show');
}
var activeTab = localStorage.getItem('activeTab');
if (activeTab) {
  $('a[href="' + activeTab + '"]').tab('show');
}

$('body').on('click', 'a[data-toggle=\'tab\']', function (e) {
  e.preventDefault()
  var tab_name = this.getAttribute('href')
  if (history.pushState) {
    history.pushState(null, null, tab_name)
  }
  else {
    location.hash = tab_name
  }
  localStorage.setItem('activeTab', tab_name)

  $(this).tab('show');
  return false;
});

$(window).on('popstate', function () {
  var anchor = location.hash ||
    $('a[data-toggle=\'tab\']').first().attr('href');
  $('a[href=\'' + anchor + '\']').tab('show');
});

// Init the global websocket connection
var socket = new ReconnectingWebSocket(
    (SETTINGS.DEBUG ? 'ws://' : 'wss://')
    + window.location.host + '/ws/'
);
window.socket = socket;

socket.onclose = function (e) {
  console.error('Chat socket closed unexpectedly');
};

socket.onmessage = function (e) {
  var data;
  try {
    data = JSON.parse(e.data);
  } catch ( e ) {
    console.error(e);
    return;
  }

  if ( SETTINGS.DEBUG ) {
    console.debug(data);
  }

  // TODO: error handling
  var split = data.type.split('.');
  var namespace = split[0];
  if ( namespace in this._handlers ) {
    this._handlers[namespace].forEach(function(handler) {
      handler.onmessage(data);
    });
  }
}.bind(socket);

socket._handlers = {};

socket.register = function (namespace, handler) {
  if ( namespace in this._handlers ) {
    this._handlers[namespace].push(handler);
  } else {
    this._handlers[namespace] = [handler];
  }
  if ( socket.readyState === 'OPEN' ) {
    handler.onopen();
  }
}.bind(socket);

socket.onopen = function (event) {
  if ( SETTINGS.DEBUG ) {
    console.debug('ws connected');
  }
  // If there are registered handlers, init them
  for ( var namespace in this._handlers ) {
    this._handlers[namespace].forEach(function(handler) {
      handler.onopen();
    });
  }
}.bind(socket);
