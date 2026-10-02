from unittest.mock import Mock, patch
from django.test import SimpleTestCase, override_settings
from requests import RequestException

from catalog.services import jikan_service


@override_settings(JIKAN_API_BASE_URL='https://api.jikan.moe/v4')
class JikanServiceTests(SimpleTestCase):
    def setUp(self):
        jikan_service._CACHE.clear()

    @patch('catalog.services.jikan_service._SESSION.get')
    def test_retry_on_rate_limit_then_success(self, mock_get):
        rate_limited = Mock(status_code=429)
        success = Mock(status_code=200)
        success.json.return_value = {'data': [{'mal_id': 1}]}
        mock_get.side_effect = [rate_limited, success]

        with patch('catalog.services.jikan_service.time.sleep') as mock_sleep:
            data = jikan_service._safe_request('/top/anime', params={'limit': 1})

        self.assertEqual(data, {'data': [{'mal_id': 1}]})
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once_with(jikan_service.RETRY_BACKOFF_SECONDS)

    @patch('catalog.services.jikan_service._SESSION.get')
    def test_retry_on_request_exception_then_success(self, mock_get):
        success = Mock(status_code=200)
        success.json.return_value = {'data': [{'mal_id': 2}]}
        mock_get.side_effect = [RequestException('timeout'), success]

        with patch('catalog.services.jikan_service.time.sleep') as mock_sleep:
            data = jikan_service._safe_request('/top/manga', params={'limit': 1})

        self.assertEqual(data, {'data': [{'mal_id': 2}]})
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once_with(jikan_service.RETRY_BACKOFF_SECONDS)

    @patch('catalog.services.jikan_service._SESSION.get')
    def test_cache_hit_skips_second_http_request(self, mock_get):
        success = Mock(status_code=200)
        success.json.return_value = {'data': [{'mal_id': 3}]}
        mock_get.return_value = success

        first = jikan_service._safe_request('/top/anime', params={'limit': 1})
        second = jikan_service._safe_request('/top/anime', params={'limit': 1})

        self.assertEqual(first, second)
        self.assertEqual(mock_get.call_count, 1)

    @patch('catalog.services.jikan_service._SESSION.get')
    def test_returns_none_after_exhausting_retries(self, mock_get):
        mock_get.return_value = Mock(status_code=503)

        with patch('catalog.services.jikan_service.time.sleep') as mock_sleep:
            data = jikan_service._safe_request('/top/anime', params={'limit': 1})

        self.assertIsNone(data)
        self.assertEqual(mock_get.call_count, jikan_service.MAX_RETRIES)
        self.assertEqual(mock_sleep.call_count, jikan_service.MAX_RETRIES - 1)
