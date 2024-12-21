from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Proficiency, ProficiencyClass, ProficiencyRace
from api.models import Class, Race, Subrace


class ProficiencyEndpointTests(APITestCase):
    def setUp(self):
        # Create related objects
        self.class_obj = Class.objects.create(index="fighter", name="Fighter", hit_die=10)
        self.race = Race.objects.create(index="human", name="Human", speed=30, age="Varies",

                                        alignment="Neutral", language_desc="Common",
                                        size="Medium", size_description="Average height and weight")
        self.subrace = Subrace.objects.create(index="variant_human", name="Variant Human", desc="Versatile humans",
                                              race=self.race)

        # Create Proficiency objects
        self.proficiency1 = Proficiency.objects.create(index="light_armor", name="Light Armor", type="Armor")
        self.proficiency2 = Proficiency.objects.create(index="heavy_armor", name="Heavy Armor", type="Armor")

        # Create relationships
        ProficiencyClass.objects.create(class_obj=self.class_obj, proficiency=self.proficiency1)
        ProficiencyRace.objects.create(race=self.race, proficiency=self.proficiency1)
        ProficiencyRace.objects.create(subrace=self.subrace, proficiency=self.proficiency2)

        # Define URLs
        self.proficiencies_url = reverse("proficiency-list")
        self.proficiency_detail_url = reverse("proficiency-detail", args=[self.proficiency1.id])

    def test_list_proficiencies(self):
        response = self.client.get(self.proficiencies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check the total number of proficiencies
        self.assertEqual(response.data[0]["name"], "Light Armor")

    def test_retrieve_proficiency(self):
        response = self.client.get(self.proficiency_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Light Armor")
        self.assertEqual(response.data["type"], "Armor")
        # Check related fields
        self.assertIn("proficiency_classes", response.data)
        self.assertIn("races_and_subraces", response.data)

    def test_create_proficiency(self):
        data = {"index": "medium_armor", "name": "Medium Armor", "type": "Armor"}
        response = self.client.post(self.proficiencies_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proficiency.objects.count(), 3)
        new_proficiency = Proficiency.objects.get(index="medium_armor")
        self.assertEqual(new_proficiency.name, "Medium Armor")
        self.assertEqual(new_proficiency.type, "Armor")

    def test_update_proficiency(self):
        data = {"name": "Lightweight Armor"}
        response = self.client.patch(self.proficiency_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proficiency1.refresh_from_db()
        self.assertEqual(self.proficiency1.name, "Lightweight Armor")

    def test_delete_proficiency(self):
        response = self.client.delete(self.proficiency_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Proficiency.objects.count(), 1)

    def test_create_proficiency_with_relationships(self):
        data = {
            "index": "stealth",
            "name": "Stealth",
            "type": "Skill",
            "associated_classes": [self.class_obj.id],  # Correctly passing Class IDs
        }
        response = self.client.post(self.proficiencies_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Fetch the newly created proficiency
        proficiency = Proficiency.objects.get(index="stealth")
        # Validate that ProficiencyClass relationships are established
        self.assertEqual(ProficiencyClass.objects.filter(proficiency=proficiency).count(), 1)

    def test_invalid_create_proficiency(self):
        data = {"index": "light_armor", "name": "Duplicate Light Armor", "type": "Armor"}
        response = self.client.post(self.proficiencies_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("index", response.data)
