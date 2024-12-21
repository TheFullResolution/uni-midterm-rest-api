from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Subclass, SubclassDescription, Class


class SubclassEndpointTests(APITestCase):
    def setUp(self):
        # Create a parent class
        self.class_obj = Class.objects.create(index="wizard", name="Wizard", hit_die=6)

        # Create a subclass
        self.subclass = Subclass.objects.create(
            index="evocation",
            name="Evocation Wizard",
            subclass_flavor="Evocation",
            class_obj=self.class_obj
        )

        # Create a description for the subclass
        self.description = SubclassDescription.objects.create(
            subclass=self.subclass,
            value="A subclass focusing on evocation spells."
        )

        # Define URLs for testing
        self.subclass_list_url = reverse("subclass-list")
        self.subclass_detail_url = reverse("subclass-detail", args=[self.subclass.id])

    def test_list_subclasses(self):
        """
        Test listing all subclasses.
        """
        response = self.client.get(self.subclass_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one subclass is listed
        self.assertEqual(response.data[0]["name"], "Evocation Wizard")

    def test_retrieve_subclass(self):
        """
        Test retrieving detailed information about a subclass.
        """
        response = self.client.get(self.subclass_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Evocation Wizard")
        self.assertEqual(response.data["subclass_flavor"], "Evocation")
        self.assertIn("description", response.data)
        self.assertEqual(response.data["description"]["value"], "A subclass focusing on evocation spells.")
        self.assertIn("class_info", response.data)
        self.assertEqual(response.data["class_info"]["name"], "Wizard")

    def test_create_subclass(self):
        """
        Test creating a new subclass.
        """
        data = {
            "index": "abjuration",
            "name": "Abjuration Wizard",
            "subclass_flavor": "Abjuration",
            "class_obj": self.class_obj.id  # Pass the parent class ID
        }
        response = self.client.post(self.subclass_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subclass.objects.count(), 2)
        new_subclass = Subclass.objects.get(index="abjuration")
        self.assertEqual(new_subclass.name, "Abjuration Wizard")
        self.assertEqual(new_subclass.class_obj, self.class_obj)

    def test_update_subclass(self):
        """
        Test updating an existing subclass.
        """
        data = {"name": "Advanced Evocation Wizard"}
        response = self.client.patch(self.subclass_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subclass.refresh_from_db()
        self.assertEqual(self.subclass.name, "Advanced Evocation Wizard")

    def test_delete_subclass(self):
        """
        Test deleting a subclass.
        """
        response = self.client.delete(self.subclass_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subclass.objects.count(), 0)
