"""Pet type definitions and evolution paths."""
from typing import Dict, List

# Define all pet types and their evolution chains using actual image files
PET_TYPES = {
    "blue": {
        "name": "Blue Pet",
        "emoji": "🔵",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/blue egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/blue newborn.png"},
            3: {"species": "kid", "emoji": "🐤", "image": "/static/images/characters/blue kid.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/blue teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/blue adult.png"},
            12: {"species": "final_form", "emoji": "✨", "image": "/static/images/characters/blue final form.png"},
        }
    },
    "cherry": {
        "name": "Cherry Pet",
        "emoji": "🍒",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/blue egg.png"},  # reuse egg
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/cherry newborn.png"},
            3: {"species": "kid", "emoji": "🐤", "image": "/static/images/characters/cherry kid.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/cherry teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/cherry adult.png"},
            12: {"species": "final_form", "emoji": "✨", "image": "/static/images/characters/cherry adult.png"},  # fallback
        }   
    },
    "cyan": {
        "name": "Cyan Pet",
        "emoji": "🔷",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/blue egg.png"},  # reuse egg
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/cyan newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/cyan child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/cyan teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/cyan adult.png"},
            12: {"species": "final_form", "emoji": "✨", "image": "/static/images/characters/cyan adult.png"},  # fallback
        }
    },
    "dark_blue": {
        "name": "Dark Blue Pet",
        "emoji": "🔵",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/blue egg.png"},  # reuse egg
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/dark blue newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/dark blue child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/dark blue teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/dark blue adult.png"},
            12: {"species": "final_form", "emoji": "✨", "image": "/static/images/characters/dark blue adult.png"},  # fallback
        }
    },
    "green": {
        "name": "Green Pet",
        "emoji": "🟢",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/blue egg.png"},  # reuse egg
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/green newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/green child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/green teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/green adult.png"},
            12: {"species": "final_form", "emoji": "✨", "image": "/static/images/characters/green adult.png"},  # fallback
        }
    },
    "purple": {
        "name": "Purple Pet",
        "emoji": "🟣",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/blue egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/purple newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/purple child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/purple teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/purple adult.png"},
            12: {"species": "final_form", "emoji": "✨", "image": "/static/images/characters/purple adult.png"},
        }
    },
}

def get_pet_type(pet_type_id: str) -> Dict:
    """Get pet type config by ID. Raises ValueError if not found."""
    if pet_type_id not in PET_TYPES:
        raise ValueError(f"Unknown pet type: {pet_type_id}")
    return PET_TYPES[pet_type_id]

def get_all_pet_types() -> List[Dict]:
    """Return list of all available pet types with basic info."""
    return [
        {
            "id": key,
            "name": value["name"],
            "emoji": value["emoji"],
            "preview_image": value["evolution_chain"][3]["image"]  # Show kid stage as preview
        }
        for key, value in PET_TYPES.items()
    ]

def get_species_for_level(pet_type_id: str, level: int) -> Dict:
    """
    Get the species, emoji, and image for a given pet type at a specific level.
    Returns {"species": str, "emoji": str, "image": str}
    """
    pet_type = get_pet_type(pet_type_id)
    evolution_chain = pet_type["evolution_chain"]

    # Find the highest level threshold that doesn't exceed current level
    current_species = None
    for level_threshold in sorted(evolution_chain.keys()):
        if level >= level_threshold:
            current_species = evolution_chain[level_threshold]

    return current_species or evolution_chain[1]
