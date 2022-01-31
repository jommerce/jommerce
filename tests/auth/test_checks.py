from django.test import TestCase, override_system_checks, override_settings
from jommerce.auth.checks import check_superuser_id
from jommerce.auth.models import User
from django.core import checks


@override_system_checks([check_superuser_id])
class SuperuserIdChecks(TestCase):
    def test_check_superuser_id_type(self):
        expected_error = checks.Error(
            "'AUTH_SUPERUSER_ID' must be an integer", id="auth.E001"
        )
        for type_ in ("invalid", 3.14, [], {}, set(), None):
            with self.settings(AUTH_SUPERUSER_ID=type_):
                self.assertEqual(checks.run_checks(), [expected_error])

    @override_settings(AUTH_SUPERUSER_ID=1)
    def test_when_database_is_empty_and_superuser_id_is_1(self):
        self.assertEqual(checks.run_checks(), [])

    def test_check_superuser_id_exists_or_not_exists(self):
        def expected_error(id_):
            return checks.Error(
                f"Couldn't find User with id={id_}",
                hint="Change the 'AUTH_SUPERUSER_ID' value or create a user with that ID.",
                obj=User,
                id="auth.E002",
            )

        # when database is empty and superuser id is not 1
        with self.settings(AUTH_SUPERUSER_ID=0):
            self.assertEqual(checks.run_checks(), [expected_error(0)])
        with self.settings(AUTH_SUPERUSER_ID=2):
            self.assertEqual(checks.run_checks(), [expected_error(2)])

        # when database is not empty and superuser id is 1
        User.objects.get_or_create(id=0, email="user0@gmail.com", password="123456")
        with self.settings(AUTH_SUPERUSER_ID=1):
            self.assertEqual(checks.run_checks(), [expected_error(1)])
        User.objects.create(id=1, email="user1@gmail.com", password="123456")
        with self.settings(AUTH_SUPERUSER_ID=1):
            self.assertEqual(checks.run_checks(), [])

        # when database is not empty and superuser id is not 1
        User.objects.get_or_create(id=0, email="user0@gmail.com", password="123456")
        with self.settings(AUTH_SUPERUSER_ID=2):
            self.assertEqual(checks.run_checks(), [expected_error(2)])
        User.objects.create(id=2, email="user2@gmail.com", password="123456")
        with self.settings(AUTH_SUPERUSER_ID=2):
            self.assertEqual(checks.run_checks(), [])
