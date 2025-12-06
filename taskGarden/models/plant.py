# models/plant.py

class Plant:
    """
    Represents a plant in the user's TaskGarden.

    Each category has one plant associated with it. The plant grows whenever
    the user completes tasks in that category.

    Attributes
    ----------
    species : str
        The type/species of the plant (e.g., "Rose", "Bamboo").
    growth_level : int
        Integer index representing which growth stage the plant is in.
        Starts at 0 and increases as tasks are completed.

    Class Attributes
    ----------------
    GROWTH_STAGES : list[str]
        Emoji-based growth stages from seedling to full plant.
    """

    # Possible plant growth stages, displayed when viewing the garden
    GROWTH_STAGES = ["🌱", "🌿", "🌳"]

    def __init__(self, species):
        """
        Initialize a new Plant.

        Parameters
        ----------
        species : str
            The plant species/name associated with this category.
        """
        self.species = species
        self.growth_level = 0  # plants always start at the first stage

    # ------------------- Growth Logic -------------------

    def grow(self):
        """
        Increase the plant's growth level by one stage.

        Growth only happens if the plant has not yet reached the final stage.
        This method is called whenever the user completes a task assigned to
        the plant's category.
        """
        if self.growth_level < len(self.GROWTH_STAGES) - 1:
            self.growth_level += 1

    def get_stage(self):
        """
        Retrieve the current emoji representing the plant's growth stage.

        Returns
        -------
        str
            A seedling/leaf/tree emoji depending on growth_level.
        """
        return self.GROWTH_STAGES[self.growth_level]

    # ------------------- Serialization -------------------

    def to_dict(self):
        """
        Convert the Plant into a dictionary for JSON storage.

        Returns
        -------
        dict
            A JSON-friendly dictionary containing species and growth_level.
        """
        return {
            "species": self.species,
            "growth_level": self.growth_level
        }

    @classmethod
    def from_dict(cls, data):
        """
        Restore a Plant object from stored dictionary data.

        Parameters
        ----------
        data : dict
            A dictionary created by `to_dict()`.

        Returns
        -------
        Plant
            A fully restored Plant object with correct species and growth level.
        """
        plant = cls(data.get("species", ""))
        plant.growth_level = data.get("growth_level", 0)
        return plant
