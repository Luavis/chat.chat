"use strict";

(function() {
    var chatApp = angular.module('chatchat', []);

    chatApp.controller('ChatController', function($scope, $element) {
        $scope.msgs = [{'text': "Hello World", 'time': '05:09:02'}];

        var socket = io.connect("http://localhost:5000/msg");
        var msgDOM = $element[0].getElementsByClassName('chat-content-wrap')[0];

        socket.on('recv_msg', function(data) {
            var timestamp = new Date().getTime() / 1000;
            console.log(((timestamp - data.timestamp) * 1000) + 'ms')
            $scope.msgs.push(angular.copy(data));

            $scope.$apply();
            msgDOM.scrollTop = msgDOM.scrollHeight
        });

        $scope.send_msg = function() {
            var timestamp = new Date().getTime() / 1000;
            socket.emit('send_msg', {msg: $scope.new_msg, timestamp: timestamp});
        }
    });
})();
