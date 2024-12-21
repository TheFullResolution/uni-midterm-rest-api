from django.db import models

from .classes import Class


# Represents a subclass associated with a specific class.
class Subclass(models.Model):
    # Unique identifier for the subclass, used as a reference.
    index = models.CharField(max_length=50, unique=True)
    # ForeignKey linking the subclass to its parent class. Uses CASCADE to delete subclasses if the parent class is deleted.
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subclasses")
    # Name of the subclass, e.g., "Evocation Wizard".
    name = models.CharField(max_length=100)
    # Flavor or theme of the subclass, e.g., "Evocation" or "Shadow".
    subclass_flavor = models.CharField(max_length=100)

    def __str__(self):
        # Returns the name of the subclass when represented as a string.
        return self.name


# Represents a detailed description for a specific subclass.
class SubclassDescription(models.Model):
    # One-to-one relationship to a subclass, ensuring each subclass has at most one description.
    subclass = models.OneToOneField(Subclass, on_delete=models.CASCADE, related_name="description")
    # The actual description content, typically text-based.
    value = models.TextField()
