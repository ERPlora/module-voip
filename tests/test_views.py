"""Tests for voip views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('voip:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('voip:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('voip:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestCallLogViews:
    """CallLog view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('voip:call_logs_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('voip:call_logs_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('voip:call_logs_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('voip:call_logs_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('voip:call_logs_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('voip:call_logs_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('voip:call_log_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('voip:call_log_add')
        data = {
            'caller_number': 'New Caller Number',
            'callee_number': 'New Callee Number',
            'direction': 'New Direction',
            'status': 'New Status',
            'started_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, call_log):
        """Test edit form loads."""
        url = reverse('voip:call_log_edit', args=[call_log.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, call_log):
        """Test editing via POST."""
        url = reverse('voip:call_log_edit', args=[call_log.pk])
        data = {
            'caller_number': 'Updated Caller Number',
            'callee_number': 'Updated Callee Number',
            'direction': 'Updated Direction',
            'status': 'Updated Status',
            'started_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, call_log):
        """Test soft delete via POST."""
        url = reverse('voip:call_log_delete', args=[call_log.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        call_log.refresh_from_db()
        assert call_log.is_deleted is True

    def test_bulk_delete(self, auth_client, call_log):
        """Test bulk delete."""
        url = reverse('voip:call_logs_bulk_action')
        response = auth_client.post(url, {'ids': str(call_log.pk), 'action': 'delete'})
        assert response.status_code == 200
        call_log.refresh_from_db()
        assert call_log.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('voip:call_logs_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('voip:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('voip:settings')
        response = client.get(url)
        assert response.status_code == 302

