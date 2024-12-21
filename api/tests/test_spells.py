from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Spell, SpellDescription, SpellClass, SpellSubclass, School, Class, Subclass


class SpellEndpointTests(APITestCase):
    def setUp(self):
        # Create a school
        self.school = School.objects.create(index="evocation", name="Evocation")

        # Create a spell
        self.spell = Spell.objects.create(
            index="fireball",
            name="Fireball",
            level=3,
            attack_type="Ranged",
            casting_time="1 action",
            concentration=False,
            duration="Instantaneous",
            material="A tiny ball of bat guano and sulfur",
            range="150 feet",
            ritual=False,
            school=self.school
        )

        # Create descriptions for the spell
        self.description1 = SpellDescription.objects.create(spell=self.spell,
                                                            value="A bright streak flashes from your pointing finger to a point you choose.")
        self.description2 = SpellDescription.objects.create(spell=self.spell,
                                                            value="Then blossoms with a low roar into an explosion of flame.")

        # Create a class and associate it with the spell
        self.class_obj = Class.objects.create(index="wizard", name="Wizard", hit_die=6)
        SpellClass.objects.create(spell=self.spell, class_obj=self.class_obj)

        # Create a subclass and associate it with the spell
        self.subclass = Subclass.objects.create(index="evocation", name="Evocation Wizard", subclass_flavor="Evocation",
                                                class_obj=self.class_obj)
        SpellSubclass.objects.create(spell=self.spell, subclass=self.subclass)

        # Define URLs for testing
        self.spell_list_url = reverse("spell-list")
        self.spell_detail_url = reverse("spell-detail", args=[self.spell.id])

    def test_list_spells(self):
        """
        Test listing all spells.
        """
        response = self.client.get(self.spell_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one spell is listed
        self.assertEqual(response.data[0]["name"], "Fireball")

    def test_retrieve_spell(self):
        """
        Test retrieving detailed information about a spell.
        """
        response = self.client.get(self.spell_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Fireball")
        self.assertEqual(response.data["school_name"], "Evocation")
        self.assertEqual(len(response.data["descriptions"]), 2)  # Ensure descriptions are included
        self.assertEqual(response.data["descriptions"][0]["value"],
                         "A bright streak flashes from your pointing finger to a point you choose.")
        self.assertEqual(len(response.data["classes"]), 1)  # Ensure associated class is included
        self.assertEqual(response.data["classes"][0]["class_name"], "Wizard")
        self.assertEqual(len(response.data["subclasses"]), 1)  # Ensure associated subclass is included
        self.assertEqual(response.data["subclasses"][0]["subclass_name"], "Evocation Wizard")

    def test_create_spell(self):
        """
        Test creating a new spell.
        """
        data = {
            "index": "magic_missile",
            "name": "Magic Missile",
            "level": 1,
            "attack_type": "Ranged",
            "casting_time": "1 action",
            "concentration": False,
            "duration": "Instantaneous",
            "material": "A bit of fleece",
            "range": "120 feet",
            "ritual": False,
            "school": self.school.id
        }
        response = self.client.post(self.spell_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Spell.objects.count(), 2)
        new_spell = Spell.objects.get(index="magic_missile")
        self.assertEqual(new_spell.name, "Magic Missile")
        self.assertEqual(new_spell.school, self.school)

    def test_update_spell(self):
        """
        Test updating an existing spell.
        """
        data = {"name": "Super Fireball"}
        response = self.client.patch(self.spell_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.spell.refresh_from_db()
        self.assertEqual(self.spell.name, "Super Fireball")

    def test_delete_spell(self):
        """
        Test deleting a spell.
        """
        response = self.client.delete(self.spell_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Spell.objects.count(), 0)
