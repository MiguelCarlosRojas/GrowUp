/**
 * GrowUp Real-Time WebSocket Client
 * Connects to the native ASGI WebSocket endpoint for live updates
 * without repetitive polling queries to the database.
 */
(function() {
    'use strict';

    let socket = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    let pingInterval = null;

    function getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${protocol}//${window.location.host}/ws/live/`;
    }

    function initWebSocket() {
        if (!('WebSocket' in window)) {
            // Fallback to single-query REST API if WebSockets not supported
            fetchFallbackMetrics();
            return;
        }

        try {
            const url = getWebSocketUrl();
            socket = new WebSocket(url);

            socket.onopen = function() {
                reconnectAttempts = 0;
                // Subscribe to live metric events
                socket.send(JSON.stringify({ action: 'subscribe', topic: 'global' }));
                
                // Ping keep-alive
                if (pingInterval) clearInterval(pingInterval);
                pingInterval = setInterval(function() {
                    if (socket && socket.readyState === WebSocket.OPEN) {
                        socket.send(JSON.stringify({ action: 'ping' }));
                    }
                }, 25000);
            };

            socket.onmessage = function(event) {
                try {
                    const message = JSON.parse(event.data);
                    if (message.event === 'live_metrics' && message.data) {
                        updateLiveElements(message.data);
                    } else if (message.event === 'live_notifications' && Array.isArray(message.notifications)) {
                        displayLiveNotifications(message.notifications);
                    }
                } catch (e) {
                    // Ignore malformed payloads
                }
            };

            socket.onclose = function() {
                if (pingInterval) clearInterval(pingInterval);
                if (reconnectAttempts < maxReconnectAttempts) {
                    const timeout = Math.min(1000 * Math.pow(2, reconnectAttempts), 15000);
                    reconnectAttempts++;
                    setTimeout(initWebSocket, timeout);
                } else {
                    fetchFallbackMetrics();
                    fetchFallbackNotifications();
                }
            };

            socket.onerror = function() {
                if (socket) socket.close();
            };

        } catch (err) {
            fetchFallbackMetrics();
            fetchFallbackNotifications();
        }
    }

    function displayLiveNotifications(notifications) {
        if (!Array.isArray(notifications) || !window.showToast) return;
        notifications.slice(0, 2).forEach(function(item, idx) {
            setTimeout(function() {
                window.showToast(
                    item.text,
                    item.type || 'info',
                    item.duration || 5000,
                    item.title,
                    item.icon
                );
            }, 600 + (idx * 1400));
        });
    }

    function updateLiveElements(data) {
        document.querySelectorAll('[data-ws-live]').forEach(function(el) {
            const key = el.getAttribute('data-ws-live');
            if (data[key] !== undefined) {
                el.textContent = data[key];
            }
        });
    }

    function fetchFallbackMetrics() {
        fetch('/api/live/metrics/')
            .then(function(res) { return res.json(); })
            .then(function(payload) {
                if (payload.status === 'success' && payload.metrics) {
                    updateLiveElements(payload.metrics);
                }
            })
            .catch(function() {
                // Silently ignore network failures
            });
    }

    function fetchFallbackNotifications() {
        fetch('/api/live/notifications/')
            .then(function(res) { return res.json(); })
            .then(function(payload) {
                if (payload.status === 'success' && Array.isArray(payload.notifications)) {
                    displayLiveNotifications(payload.notifications);
                }
            })
            .catch(function() {
                // Silently ignore network failures
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWebSocket);
    } else {
        initWebSocket();
    }
})();
