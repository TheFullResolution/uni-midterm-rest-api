from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import School, Spell


class SchoolEndpointTests(APITestCase):
    def setUp(self):
        # Create School instances
        self.school1 = School.objects.create(index="evocation", name="Evocation")
        self.school2 = School.objects.create(index="necromancy", name="Necromancy")

        # Create Spell instances and associate them with schools
        self.spell1 = Spell.objects.create(
            index="fireball", name="Fireball", level=3, attack_type="Ranged",
            casting_time="1 action", concentration=False, duration="Instantaneous",
            material="A tiny ball of bat guano and sulfur", range="150 feet",
            ritual=False, school=self.school1
        )
        self.spell2 = Spell.objects.create(
            index="magic_missile", name="Magic Missile", level=1, attack_type="Ranged",
            casting_time="1 action", concentration=False, duration="Instantaneous",
            material=None, range="120 feet", ritual=False, school=self.school1
        )

        # URLs for endpoints
        self.school_list_url = reverse("school-list")
        self.school_detail_url = reverse("school-detail", args=[self.school1.id])

    def test_list_schools(self):
        """
        Test the list endpoint for schools.
        """
        response = self.client.get(self.school_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure both schools are listed
        self.assertEqual(response.data[0]["name"], "Evocation")

    def test_retrieve_school(self):
        """
        Test the detail endpoint for a specific school.
        """
        response = self.client.get(self.school_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Evocation")
        self.assertEqual(len(response.data["spells"]), 2)  # Ensure spells are listed
        self.assertEqual(response.data["spells"][0]["name"], "Fireball")

    def test_create_school(self):
        """
        Test creating a new school.
        """
        data = {"index": "transmutation", "name": "Transmutation"}
        response = self.client.post(self.school_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 3)
        new_school = School.objects.get(index="transmutation")
        self.assertEqual(new_school.name, "Transmutation")

    def test_update_school(self):
        """
        Test updating an existing school.
        """
        data = {"name": "Advanced Evocation"}
        response = self.client.patch(self.school_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school1.refresh_from_db()
        self.assertEqual(self.school1.name, "Advanced Evocation")

    def test_delete_school(self):
        """
        Test deleting a school.
        """
        response = self.client.delete(self.school_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(School.objects.count(), 1)

    def test_school_with_spells(self):
        """
        Test the relationship between schools and spells.
        """
        response = self.client.get(self.school_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["spells"]), 2)
        self.assertEqual(response.data["spells"][0]["name"], "Fireball")
        self.assertEqual(response.data["spells"][1]["name"], "Magic Missile")
