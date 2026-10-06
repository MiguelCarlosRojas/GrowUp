/**
 * GrowUp Real-Time WebSocket Client
 * Connects to ASGI WebSocket endpoint for live updates.
 * Gracefully and immediately falls back to REST API if WebSockets
 * are unavailable or unsupported by the hosting environment.
 */
(function() {
    'use strict';

    let socket = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 2;
    let pingInterval = null;
    let hasEverConnected = false;

    function getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${protocol}//${window.location.host}/ws/live/`;
    }

    function initWebSocket() {
        // Immediate fallback fetching ensures metrics and notifications populate without waiting
        fetchFallbackMetrics();
        fetchFallbackNotifications();

        if (!('WebSocket' in window)) {
            return;
        }

        // If WebSockets were verified unavailable on this host in the current session, do not attempt
        try {
            if (sessionStorage.getItem('growup_ws_available') === 'false') {
                return;
            }
        } catch (e) {
            // Storage access restricted, proceed
        }

        try {
            const url = getWebSocketUrl();
            socket = new WebSocket(url);

            socket.onopen = function() {
                hasEverConnected = true;
                reconnectAttempts = 0;
                try {
                    sessionStorage.setItem('growup_ws_available', 'true');
                } catch (e) {}

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

                if (!hasEverConnected) {
                    // Handshake failed or server environment (e.g. WSGI) does not support WebSockets.
                    // Mark as unavailable for session and DO NOT retry to prevent console error loops.
                    try {
                        sessionStorage.setItem('growup_ws_available', 'false');
                    } catch (e) {}
                    return;
                }

                // If previously connected and dropped due to a transient network blip, retry once or twice
                if (reconnectAttempts < maxReconnectAttempts) {
                    const timeout = Math.min(1000 * Math.pow(2, reconnectAttempts), 10000);
                    reconnectAttempts++;
                    setTimeout(initWebSocket, timeout);
                }
            };

            socket.onerror = function() {
                if (socket) {
                    try {
                        socket.close();
                    } catch (e) {}
                }
            };

        } catch (err) {
            try {
                sessionStorage.setItem('growup_ws_available', 'false');
            } catch (e) {}
        }
    }

    function displayLiveNotifications(notifications) {
        if (!Array.isArray(notifications)) return;

        // Update topbar notification dropdowns in real time
        notifications.forEach(function(item) {
            if (item.type === 'review') {
                const el = document.getElementById('topbarReviewText');
                if (el && item.text) el.textContent = item.text;
            } else if (item.type === 'discussion') {
                const el = document.getElementById('topbarDiscussionText');
                if (el && item.text) el.textContent = item.text;
            }
        });

        if (!window.showToast) return;
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
