"use strict";

(function() {
    var chatApp = angular.module('chatchat', []);

    chatApp.controller('ChatController', function($scope, $element, $http) {
        $scope.msgs = [];

        var msgDOM = $element[0].getElementsByClassName('chat-content-wrap')[0];

        (function send_msg() {
            $http({
                url: '/msg',
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                data: {
                    'uid': user_id
                },
                transformRequest: function(obj) {
                    var str = [];
                    for(var p in obj)
                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                    return str.join("&");
                }
            }).success(function(data, status, headers, config) {
                if(data){
                    if(data.status == 'success') {
                        var timestamp = new Date().getTime() / 1000;
                        console.log(((timestamp - data.timestamp) * 1000) + 'ms');
                        $scope.msgs.push(angular.copy(data));
                        msgDOM.scrollTop = msgDOM.scrollHeight
                    }
                }

                send_msg()
            }).error(function() {
                setTimeout(send_msg, 5)
            })
        })()

        $scope.send_msg = function() {
            
            if($scope.new_msg.length == 0 ||
               $scope.new_msg.replace(/^[\s]+/, '').length == 0)  // pass empty message
                return;

            // var timestamp = new Date().getTime() / 1000;
            $http({
                url: '/send_msg',
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                data: {
                    'uid' : user_id,
                    'msg': $scope.new_msg
                },
                transformRequest: function(obj) {
                    var str = [];
                    for(var p in obj)
                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                    return str.join("&");
                }
            }).success(function() {

            });

            $scope.new_msg = ''
        }

    });
})();
