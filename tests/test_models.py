"""Tests for voip models."""
import pytest
from django.utils import timezone

from voip.models import CallLog


@pytest.mark.django_db
class TestCallLog:
    """CallLog model tests."""

    def test_create(self, call_log):
        """Test CallLog creation."""
        assert call_log.pk is not None
        assert call_log.is_deleted is False

    def test_soft_delete(self, call_log):
        """Test soft delete."""
        pk = call_log.pk
        call_log.is_deleted = True
        call_log.deleted_at = timezone.now()
        call_log.save()
        assert not CallLog.objects.filter(pk=pk).exists()
        assert CallLog.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, call_log):
        """Test default queryset excludes deleted."""
        call_log.is_deleted = True
        call_log.deleted_at = timezone.now()
        call_log.save()
        assert CallLog.objects.filter(hub_id=hub_id).count() == 0


