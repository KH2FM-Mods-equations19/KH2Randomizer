WEAK = "WEAK"
MILD = "MILD"
MEDIUM = "MEDIUM"
STRONG = "STRONG"
HEAVY = "HEAVY"
OVERPOWERED = "OVERPOWERED"
CHAOS = "CHAOS"
NIGHTMARE = "NIGHTMARE"
DISABLED = "DISABLED"

class AttackDataPresets:

    def __init__(self, attack_data_preset_choice: str):
        super().__init__()
        self.attack_data_preset_choice = attack_data_preset_choice

    @staticmethod
    def attack_data_preset_options() -> dict[str, str]:
        return {
            WEAK: "WEAK",
            MILD: "MILD",
            MEDIUM: "MEDIUM",
            STRONG: "STRONG",
            HEAVY: "HEAVY",
            OVERPOWERED: "OVERPOWERED",
            NIGHTMARE: "NIGHTMARE",
            CHAOS: "CHAOS",
            DISABLED: "DISABLED",
        }

    @staticmethod
    def attack_data_preset_tooltip() -> str:
        return """
        Influences the strength of which these values are randomized.
        PRESET          MIN    MAX  (multiplier)
        Weak =          1.0x - 1.3x difference
        Mild =          1.0x - 1.5x
        Medium =        1.2x - 1.8x
        Strong =        1.5x - 2.2x
        Heavy =         1.8x - 3.0x
        Overpowered =   2.2x - 4.0x
        Nightmare =     3.4 - 6.0x
        Chaos =         1.0x - 9.0x

        Remember that the difference can be either positive or negative.
        Revenge Value is handled differently.
        """
    
    @staticmethod
    def multi_hit_preset_tooltip() -> str:
        return """
        Potentially changes moves to do multiple hits and how
        frequently they hit
        PRESET      chance for move change
        Weak =          5%
        Mild =          8%
        Medium =        12%
        Strong =        25%
        Heavy =         35%
        Overpowered =   40%
        Nightmare =     60%
        Chaos =         90%

        The presets influence 2 things: how likely a move becomes a multi hit 
        and the rate of its hits. Generally speaking, can make the game very 
        dangerous if set to Heavy or higher.
        """
    
    @staticmethod
    def hpdrain_preset_tooltip() -> str:
        return """
        Potentially changes moves to heal self when hitting an enemy
        PRESET      chance for move change
        Weak =          10%
        Mild =          16%
        Medium =        24%
        Strong =        30%
        Heavy =         40%
        Overpowered =   50%
        Nightmare =     80%
        Chaos =         100%

        The presets influence 2 things: how likely a move is changed to heal self and 
        how much it heals.
        """