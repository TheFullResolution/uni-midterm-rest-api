from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Class, Proficiency, ClassProficiency, Subclass


class ClassEndpointTests(APITestCase):
    def setUp(self):
        # Create some proficiencies
        self.proficiency1 = Proficiency.objects.create(index="proficiency_1", name="Light Armor", type="Armor")
        self.proficiency2 = Proficiency.objects.create(index="proficiency_2", name="Heavy Armor", type="Armor")

        # Create a class
        self.class1 = Class.objects.create(index="wizard", name="Wizard", hit_die=6)
        ClassProficiency.objects.create(class_obj=self.class1, proficiency=self.proficiency1)
        ClassProficiency.objects.create(class_obj=self.class1, proficiency=self.proficiency2)

        # Create a subclass
        self.subclass1 = Subclass.objects.create(
            index="evocation", name="Evocation Wizard", subclass_flavor="Evocation", class_obj=self.class1
        )

        # URLs
        self.classes_url = reverse("class-list")
        self.class_detail_url = reverse("class-detail", args=[self.class1.id])

    def test_list_classes(self):
        response = self.client.get(self.classes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one class created
        self.assertEqual(response.data[0]["name"], "Wizard")

    def test_retrieve_class(self):
        response = self.client.get(self.class_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Wizard")
        self.assertEqual(len(response.data["class_proficiencies"]), 2)
        self.assertEqual(response.data["subclasses"][0]["name"], "Evocation Wizard")

    def test_create_class(self):
        data = {
            "index": "test_class",
            "hit_die": 10,
            "name": "Fighter Test",
            "proficiencies": [self.proficiency1.id, self.proficiency2.id],
        }
        response = self.client.post(self.classes_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Class.objects.count(), 2)  # One already created in setUp
        new_class = Class.objects.get(index="test_class")
        self.assertEqual(new_class.name, "Fighter Test")
        self.assertEqual(new_class.hit_die, 10)

    def test_update_class(self):
        data = {"name": "Advanced Wizard"}
        response = self.client.patch(self.class_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.class1.refresh_from_db()
        self.assertEqual(self.class1.name, "Advanced Wizard")

    def test_delete_class(self):
        response = self.client.delete(self.class_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Class.objects.count(), 0)

    def test_create_class_with_duplicate_index(self):
        data = {"index": "wizard", "hit_die": 8, "name": "Duplicate Wizard"}
        response = self.client.post(self.classes_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("index", response.data)

    def test_create_class_invalid_hit_die(self):
        data = {"index": "monk", "hit_die": "invalid", "name": "Monk"}
        response = self.client.post(self.classes_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("hit_die", response.data)

    def test_create_class_with_invalid_proficiency(self):
        data = {
            "index": "cleric",
            "hit_die": 8,
            "name": "Cleric",
            "proficiencies": [999],  # Invalid ID
        }
        response = self.client.post(self.classes_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("proficiencies", response.data)
