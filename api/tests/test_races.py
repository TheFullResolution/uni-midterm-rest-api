from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Race, Subrace, Proficiency, RaceStartingProficiency, SubraceStartingProficiency


class RaceEndpointTests(APITestCase):
    def setUp(self):
        # Create some proficiency objects
        self.proficiency1 = Proficiency.objects.create(index="light_armor", name="Light Armor", type="Armor")
        self.proficiency2 = Proficiency.objects.create(index="stealth", name="Stealth", type="Skill")

        # Create a Race object
        self.race = Race.objects.create(
            index="human", name="Human", speed=30, age="Adult at 18; lives up to 80 years.",
            alignment="Neutral", language_desc="Common", size="Medium", size_description="Average height and weight"
        )

        # Create a Subrace object
        self.subrace = Subrace.objects.create(index="variant_human", name="Variant Human", desc="Versatile humans.",
                                              race=self.race)

        # Create starting proficiencies
        RaceStartingProficiency.objects.create(race=self.race, proficiency=self.proficiency1)
        SubraceStartingProficiency.objects.create(subrace=self.subrace, proficiency=self.proficiency2)

        # URLs
        self.race_list_url = reverse("race-list")
        self.race_detail_url = reverse("race-detail", args=[self.race.id])

    def test_list_races(self):
        response = self.client.get(self.race_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Human")

    def test_retrieve_race(self):
        response = self.client.get(self.race_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Human")
        self.assertEqual(response.data["speed"], 30)
        self.assertIn("starting_proficiencies", response.data)
        self.assertEqual(len(response.data["starting_proficiencies"]), 1)
        self.assertEqual(response.data["starting_proficiencies"][0]["proficiency_name"], "Light Armor")

    def test_create_race(self):
        data = {
            "index": "elf",
            "name": "Elf",
            "speed": 35,
            "age": "Mature at 100; lives up to 750 years.",
            "alignment": "Chaotic Good",
            "language_desc": "Elvish",
            "size": "Medium",
            "size_description": "Tall and slender",
        }
        response = self.client.post(self.race_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Race.objects.count(), 2)
        new_race = Race.objects.get(index="elf")
        self.assertEqual(new_race.name, "Elf")
        self.assertEqual(new_race.speed, 35)

    def test_update_race(self):
        data = {"speed": 25}
        response = self.client.patch(self.race_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.race.refresh_from_db()
        self.assertEqual(self.race.speed, 25)

    def test_delete_race(self):
        response = self.client.delete(self.race_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Race.objects.count(), 0)

    def test_race_with_starting_proficiencies(self):
        data = {
            "index": "dwarf",
            "name": "Dwarf",
            "speed": 25,
            "age": "Adult at 50; lives up to 350 years.",
            "alignment": "Lawful Good",
            "language_desc": "Dwarvish",
            "size": "Medium",
            "size_description": "Short and sturdy",
        }
        response = self.client.post(self.race_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        dwarf_race = Race.objects.get(index="dwarf")
        RaceStartingProficiency.objects.create(race=dwarf_race, proficiency=self.proficiency1)
        response = self.client.get(reverse("race-detail", args=[dwarf_race.id]))
        self.assertEqual(len(response.data["starting_proficiencies"]), 1)
        self.assertEqual(response.data["starting_proficiencies"][0]["proficiency_name"], "Light Armor")
